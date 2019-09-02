from flask import Flask, request
from utils.Encrypt import Encrypt
import flask
from utils.InsUtils import InsUtilsWithLogin
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/publickey')
def get_public_key():
    with open('resources/public_key.pem', 'r') as file:
        key_content = file.readlines()
    q_res = {'key': key_content}
    response = flask.make_response(flask.jsonify(q_res))
    make_header(response)
    return response


@app.route('/login/<string:platform>', methods=["POST"])
def login_account(platform):
    username = request.form.get('username')
    password = request.form.get('password')
    res = False
    if platform == 'Instagram':
        ins = InsUtilsWithLogin(False)
        ins.set_account((username, password))
        res = ins.login()
    q_res = {'result': res}
    response = flask.make_response(flask.jsonify(q_res))
    make_header(response)
    return response


@app.route('/decrypt', methods=["POST"])
def decrypt_test():
    data = request.form.get('password')
    decoder = Encrypt()
    plain_text = decoder.decrypt(decoder.decodebase64(data))
    print(plain_text)
    plain_text = plain_text.decode('utf-8')
    q_res = {'text': plain_text}
    response = flask.make_response(flask.jsonify(q_res))
    make_header(response)
    return response


def make_header(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
