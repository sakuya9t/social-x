from flask import Flask, request
from flask_cors import CORS
import flask

from utils.Couch import Couch
from utils.Decryptor import decrypt
from utils.InsUtils import InsUtilsWithLogin
import json, os

from utils.TwiUtils import TwiUtilsWithLogin

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/key')
def get_public_key():
    with open('resources/public_key.pem', 'r') as file:
        data = file.read()
        return {'data': data}


@app.route('/login', methods=["POST"])
def login_account():
    data = json.loads(request.get_data())
    platform = data['platform']
    username = data['username']
    password = decrypt(data['password'])
    res = False
    instance = None
    if len(username) == 0 and len(password) == 0:
        return make_response({'result': res})
    if platform == 'Instagram':
        instance = InsUtilsWithLogin(displayed=False)
    elif platform == 'Twitter':
        instance = TwiUtilsWithLogin(displayed=False)
    if instance is None:
        return make_response({'result': False})
    instance.set_account((username, password))
    res = instance.login()
    if res:
        config_path = os.getcwd() + '/config.json'
        database = Couch(config_path, 'credential')
        database.insert(data)

    return make_response({'result': res})


@app.route('/query', methods=["POST"])
def query():
    data = json.loads(request.get_data())
    print(data)
    return "ok"


@app.route('/decrypt', methods=["POST"])
def decrypt_api():
    data = request.get_data()
    data = json.loads(data)
    message = data['message']
    return decrypt(message)


def make_response(q_res):
    response = flask.make_response(flask.jsonify(q_res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
