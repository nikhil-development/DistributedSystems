import requests
from flask import Flask, render_template, request
from time import sleep
from kafka import KafkaProducer
from json import dumps

application = Flask("__name__")

topics_id = {1: "local_uv_irradiance_index", 2: "atmo_opacity", 3: "terrestrial_date", 4: "ls", 5: "season", 6: "min_temp", 
7: "max_temp", 8: "pressure", 9: "pressure_string", 10 :"abs_humidity", 11: "wind_speed",
12: "id", 13: "sunrise", 14: "sunset", 15: "status", 16: "min_gts_temp",
17: "max_gts_temp", 18: "wind_direction", 19: "sol", 20: "unitOfMeasure", 21: "TZ_Data"}

@application.route('/publisher_home', methods = ['POST', 'GET'])
def publisher_home():
    return render_template("publisher.html")

@application.route('/publish_button', methods = ['POST', 'GET'])
def publisher():
    
    url = "https://api.maas2.apollorion.com/"
    output = requests.request("GET", url).json()
    topics_I_publish = requests.post('http://mars_broker1:8002/topics_I_publish', json = {"a": 1})
    all_topic_identifiers = topics_I_publish.json()['a']
    application.logger.info("All Topic Identifiers")
    application.logger.info(all_topic_identifiers)

    for each_topic_identifier in all_topic_identifiers:
        result = {'message': output.get(topics_id[each_topic_identifier[0]]), 'pub_identifier': 1, 'topic_identifier': each_topic_identifier[0]}
        requests.post('http://mars_broker1:8002/event', json= {'a': result})

        producer = KafkaProducer(
        bootstrap_servers=['kafka1:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8'))
        producer.send('topic_test', value=output.get(topics_id[each_topic_identifier[0]]))

    application.logger.info('Published')
    return 'Obtaining Publisher 1 Messages'

@application.route('/advertise_button', methods = ['POST', 'GET'])
def advertise_button():
    a = requests.post('http://mars_broker1:8002/max_topic')
    application.logger.info("Max topic")
    c = a.json()['a'][0][0]
    if c is None: b = 0
    else: b = c
    message = {'pub_identifier': 1, 'topic_name': topics_id[b+1], 'topic_identifier': b+1}
    requests.post('http://mars_broker1:8002/advertise', json= {'a': message})
    application.logger.info('Advertised')

    return 'Publisher 1 has advertised a new topic - ' + topics_id[b+1]

@application.route('/deadvertise', methods = ['POST', 'GET'])
def deadvertise():
    message = {'pub_id': 3, 'topic_identifier': 1}
    requests.post('http://mars_broker1:8002/deadvertise', json = {'a': message})
    application.logger.info('Deadvertise')
    return 'Publisher 1 has de-advertised a topic!'

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port='8001')