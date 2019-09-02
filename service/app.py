from flask import Flask, request
from flask_cors import CORS
from utils.Encrypt import Encrypt
import flask
from utils.InsUtils import InsUtilsWithLogin
import json

from utils.TwiUtils import TwiUtilsWithLogin

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/publickey')
def get_public_key():
    with open('resources/public_key.pem', 'r') as file:
        key_content = file.readlines()
    q_res = {'key': key_content}
    return make_response(q_res)


@app.route('/login', methods=["POST"])
def login_account():
    data = json.loads(request.get_data())
    platform = data['platform']
    username = data['username']
    password = data['password']
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
    return make_response({'result': res})


@app.route('/decrypt', methods=["POST"])
def decrypt_test():
    data = request.form.get('password')
    decoder = Encrypt()
    plain_text = decoder.decrypt(decoder.decodebase64(data))
    print(plain_text)
    plain_text = plain_text.decode('utf-8')
    q_res = {'text': plain_text}
    return make_response(q_res)

def make_response(q_res):
    response = flask.make_response(flask.jsonify(q_res))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
