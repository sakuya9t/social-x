from flask import Flask
import flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/publickey')
def get_public_key():
    key_content = ""
    with open('resources/public_key.pem', 'r') as file:
        key_content = file.readlines()
    key_content = str.join("\n", key_content)
    q_res = {'key': key_content}
    response = flask.make_response(flask.jsonify(q_res))
    make_header(response)
    return response

def make_header(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'


if __name__ == '__main__':
    app.run()
