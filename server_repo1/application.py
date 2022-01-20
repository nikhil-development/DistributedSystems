import requests
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify
import random
import mysql.connector
import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import binascii
from kafka import KafkaConsumer

application = Flask("_name_")
configuration_of_database = {'user': 'root', 'password': 'root', 'host': 'database1', 'port': '3306', 'database': 'pubsub'}

topics_id = {1: "local_uv_irradiance_index", 2: "atmo_opacity", 3: "terrestrial_date", 4: "ls", 5: "season", 6: "min_temp", 
7: "max_temp", 8: "pressure", 9: "pressure_string", 10 :"abs_humidity", 11: "wind_speed",
12: "id", 13: "sunrise", 14: "sunset", 15: "status", 16: "min_gts_temp",
17: "max_gts_temp", 18: "wind_direction", 19: "sol", 20: "unitOfMeasure", 21: "TZ_Data"}

my_topics_id = {1: "local_uv_irradiance_index", 2: "atmo_opacity", 3: "terrestrial_date", 4: "ls", 5: "season", 6: "min_temp"}

tid = {"local_uv_irradiance_index": 1, "atmo_opacity": 2, "terrestrial_date": 3, "ls": 4, "season": 5, "min_temp": 6, 
"max_temp": 7, "pressure": 8, "pressure_string": 9, "abs_humidity": 10, "wind_speed": 11,
"id": 12, "sunrise": 13, "sunset": 14, "status": 15, "min_gts_temp": 16,
"max_gts_temp": 17, "wind_direction": 18, "sol": 19, "unitOfMeasure": 20, "TZ_Data": 21}

@application.route('/get_all_topics', methods = ['GET', 'POST'])
def get_all_topics():
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    cursor.execute("SELECT topic_identifier FROM table_publishers;")
    array_topics = [x for x in cursor]
    connection.commit()
    cursor.close()
    connection.close()
    # application.logger.info(array_topics)
    a = dict()
    a['a'] = array_topics
    return jsonify(a)

@application.route('/get_notified', methods = ['GET', 'POST'])
def get_notified():

    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    sub_identifier = request.get_json(force=True)['sub_identifier']
    cursor.execute("SELECT topic_identifier FROM table_subscriptions WHERE sub_identifier=(%s);",(sub_identifier,))
    array_topics = [x for x in cursor]
    array_topics1 = [x[0] for x in array_topics]
    connection.commit()
    cursor.close()
    connection.close()

    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info("get_notified in broker 1")
    array_topics2 = []
    for each in array_topics1:
        cursor.execute("SELECT actual_message FROM table_events WHERE topic_identifier=%s;", (each,))
        msg = [x[0] for x in cursor]
        if len(msg) != 0:
            array_topics2.append(("The message for topic " + str(each) + " is " + str(msg[0])))
    connection.commit()
    cursor.close()
    connection.close()
    a = dict()
    a['a'] = array_topics2
    return jsonify(a)

@application.route('/submit_topics', methods = ['GET', 'POST'])
def submit_topics():
    many_topics = request.get_json()
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info(many_topics)
    sub_identifier = many_topics['sub_identifier']
    application.logger.info("Many topics submit_topics broker1 subs for user :"+str(sub_identifier))
    for each in many_topics['many_topics']:
        application.logger.info("Each")
        application.logger.info(each)
        if tid[each] in my_topics_id:
            cursor.execute("INSERT INTO table_subscriptions (topic_identifier, sub_identifier) VALUES (%s,%s)", (tid[each], sub_identifier))
    connection.commit()
    cursor.close()
    connection.close()
    return 'Added new topics to database'

@application.route('/unsub2', methods = ['GET', 'POST'])
def unsub2():
    application.logger.info("unsub2 in broker 1")
    r = request.get_json(force=True)['unsub']
    sub_identifier = request.get_json(force=True)['sub_identifier']
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info("R")
    application.logger.info(r)
    for each in r:
        each = tid[each]
        cursor.execute("DELETE FROM table_subscriptions where sub_identifier=(%s) and topic_identifier=(%s);", (sub_identifier,each,))
    application.logger.info("unsub2 in broker1")
    connection.commit()
    cursor.close()
    connection.close()
    return "Unsubscribed successfully!"

@application.route('/unsub1', methods = ['GET', 'POST'])
def unsub1():
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    a = dict()
    b = []
    r = request.get_json()
    cursor.execute("SELECT topic_identifier FROM table_subscriptions where sub_identifier=(%s);",(r['sub_identifier'],))
    b.extend([topics_id[x[0]] for x in cursor])
    application.logger.info("B")
    application.logger.info(b)
    a['a'] = b
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(a)

@application.route('/unsub', methods = ['GET', 'POST'])
def unsub():
    application.logger.info("unsub in broker 1")
    r = request.get_json(force=True)['a']
    application.logger.info(r)
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info("R")
    application.logger.info(r)
    cursor.execute("DELETE FROM topic_subscriptions FROM table_subscriptions where sub_identifier=1;")
    a = dict()
    a['a'] = [x for x in cursor]
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(a)

@application.route('/topics_I_publish', methods = ['GET', 'POST'])
def topics_I_publish():
    pub_identifier = request.get_json(force=True)['a']
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info("Selecting topic for this publisher")
    cursor.execute("SELECT topic_identifier FROM table_publishers WHERE pub_identifier=%s;", (pub_identifier,))
    a = dict()
    a['a'] = [x for x in cursor]
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(a)

@application.route('/advertise', methods = ['GET', 'POST'])
def advertise():

    a = request.get_json(force=True)['a']
    application.logger.info("kafka topic")

    
    

    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO table_publishers (topic_identifier, pub_identifier) VALUES (%s,%s)", (a['topic_identifier'], a['pub_identifier'],))
    connection.commit()
    cursor.close()
    connection.close()
    return "Topic saved to table_publishers"

@application.route('/event', methods = ['GET', 'POST'])
def event():
    a = request.get_json(force=True)['a']
    if a['topic_identifier'] not in my_topics_id: return ""
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO table_events (pub_identifier, topic_identifier, actual_message) VALUES (%s,%s,%s)", (a['pub_identifier'], a['topic_identifier'], a['message'],))
    connection.commit()
    cursor.close()
    connection.close()
    return "Topic saved to table_events"

@application.route('/max_topic', methods = ['GET', 'POST'])
def max_topic():
    # pub_identifier = request.get_json(force=True)['a']
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    cursor.execute("SELECT max(topic_identifier) FROM table_publishers;")
    a = dict()
    a['a'] = [x for x in cursor]
    # application.logger.error("Max_Topic" + a)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(a)

@application.route('/deadvertise', methods = ['GET', 'POST'])
def deadvertise():
    application.logger.info("deadvertise in broker 1")
    r = request.get_json(force=True)['a']
    application.logger.info(r)
    connection = mysql.connector.connect(**configuration_of_database)
    cursor = connection.cursor()
    application.logger.info("R")
    application.logger.info(r)
    cursor.execute("DELETE FROM topic_subscriptions FROM table_subscriptions where sub_identifier=1;")
    a = dict()
    a['a'] = [x for x in cursor]
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(a)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0',port='8002')