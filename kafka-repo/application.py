from flask import Flask

application = Flask("_name_")


@application.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=9092)