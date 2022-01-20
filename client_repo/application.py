import requests
from datetime import datetime
import json
import time
from flask import Flask, jsonify
from flask import request

from flask import render_template
from flask import get_template_attribute
from flask import session
from flask import url_for
import random

import binascii
from kafka import KafkaConsumer
from json import loads
from time import sleep
import random

application = Flask("_name_")
application.secret_key='adcdabcd'
sub_current = None

topics_id = {1: "local_uv_irradiance_index", 2: "atmo_opacity", 3: "terrestrial_date", 4: "ls", 5: "season", 6: "min_temp", 
7: "max_temp", 8: "pressure", 9: "pressure_string", 10 :"abs_humidity", 11: "wind_speed",
12: "id", 13: "sunrise", 14: "sunset", 15: "status", 16: "min_gts_temp",
17: "max_gts_temp", 18: "wind_direction", 19: "sol", 20: "unitOfMeasure", 21: "TZ_Data"}

tid = {"local_uv_irradiance_index": 1, "atmo_opacity": 2, "terrestrial_date": 3, "ls": 4, "season": 5, "min_temp": 6, 
"max_temp": 7, "pressure": 8, "pressure_string": 9, "abs_humidity": 10, "wind_speed": 11,
"id": 12, "sunrise": 13, "sunset": 14, "status": 15, "min_gts_temp": 16,
"max_gts_temp": 17, "wind_direction": 18, "sol": 19, "unitOfMeasure": 20, "TZ_Data": 21}

@application.route('/')
def intiialScreen():
    return render_template("login.html")

@application.route('/subscriber_home', methods = ['GET', 'POST'])
def subscriber_home():
    error = None
    application.logger.error(request.method)
    application.logger.error(request.form.getlist('Uname'))
    application.logger.error(request.form.getlist('Pass'))
    application.logger.error(type(request.form))
    application.logger.error(type(request.method))
    application.logger.error("Username and Password " + str(request.form['Uname']) + str(request.form['Pass']))
    session['user'] = int(request.form.getlist('Uname')[0])
    if request.method == 'POST':
        if (int(request.form.getlist('Uname')[0]) == 1 and int(request.form.getlist('Pass')[0]) == 1) or (int(request.form.getlist('Uname')[0]) == 2 and int(request.form.getlist('Pass')[0]) == 2) or (int(request.form.getlist('Uname')[0]) == 3 and int(request.form.getlist('Pass')[0]) == 3):
            return render_template("subscriber.html", user = int(request.form.getlist('Uname')[0]))
        else:
            return 'Invalid Credentials. Please try again.'


@application.route('/get_all_topics', methods = ['GET', 'POST'])
def get_all_topics():
    application.logger.error("get all topics in subscriber")
    application.logger.error("user info:"+ str(session['user']))
    application.logger.error(request.args)
    a = requests.get('http://mars_broker1:8002/get_all_topics')
    application.logger.error("Inside client get all topics")

    consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['kafka1:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

    for event in consumer:
     event_data = event.value
    # Do whatever you want
     print(event_data)
     sleep(2)
    # application.logger.error(a.json())
    # application.logger.error([topics_id[x[0]] for x in a.json()['a']])
    return render_template("get_all_topics.html", topics = [topics_id[x[0]] for x in a.json()['a']])

@application.route('/get_notified', methods = ['GET', 'POST'])
def get_notified():
    sub_identifier = int(session['user'])
    a = requests.get('http://mars_broker1:8002/get_notified',json = {"sub_identifier": sub_identifier})
    application.logger.error("get_notified client")
    application.logger.error(a.json())
    return render_template("get_notified.html", messages = a.json()['a'])

@application.route('/get_notified1', methods = ['GET', 'POST'])
def get_notified1():
    sub_identifier = int(session['user'])
    a = requests.get('http://mars_broker1:8002/get_notified',json = {"sub_identifier": sub_identifier})
    return jsonify(a.json())

@application.route('/submit_topics', methods = ['GET', 'POST'])
def submit_topics():
    # application.logger.error("ONE: Message below submit_topics in Client")
    many_topics = request.form.getlist('topic')
    application.logger.error("Many Topics")
    application.logger.error(many_topics)
    sub_identifier = int(session['user'])
    requests.post('http://mars_broker1:8002/submit_topics', json = {"sub_identifier": sub_identifier, "many_topics": many_topics})
    return "Subscribed!!"

@application.route('/unsub1', methods = ['GET', 'POST'])
def unsub1():
    sub_identifier = int(session['user'])
    a = requests.post('http://mars_broker1:8002/unsub1', json = {"sub_identifier":sub_identifier})
    application.logger.error("unsub1 in subscriber")
    application.logger.error(a.json()['a'])
    return render_template("unsub.html", unsub = a.json()['a'])

@application.route('/unsub2', methods = ['GET', 'POST'])
def unsub2():
    sub_identifier = int(session['user'])
    a = request.form.getlist('topic')
    application.logger.error("unsub2 in subscriber")
    application.logger.error(a)
    a = requests.post('http://mars_broker1:8002/unsub2', json = {"unsub": a,"sub_identifier":sub_identifier})
    return ""





@application.route('/publish', methods = ['POST', 'GET'])
def output():
   if request.method == 'POST':
    output = request.form
    message = {'sub': output['sub']}
    requests.post('http://mars_broker:8002/endpoint', json=message)
    return ""

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8003)