import json

import flask
from flask import Flask, request
from flask_cors import CORS

from constant import REALTIME_MODE, DATABASE_FEEDBACK, DATABASE_CREDENTIAL, \
    DATABASE_DATA_AWAIT_BATCH
from similarity.SimCalculator import SimCalculator, column_names, query_existing_similarity_in_db
from utils.Couch import Couch
from utils.Decryptor import decrypt
from utils.InsUtils import InsUtilsWithLogin
from utils.QueryGenerator import retrieve
from utils.TwiUtils import TwiUtilsWithLogin

app = Flask(__name__)
CORS(app)
algoModule = SimCalculator()


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
        database = Couch(DATABASE_CREDENTIAL)
        database.insert(data)
        database.close()

    return make_response({'result': res})


@app.route('/query', methods=["POST"])
def query():
    """
        Request format:
            {'account1': {'platform':'xxx', 'account': 'aaa'}, 'account2': {'platform':'yyy', 'account': 'bbb'}}
        Response format:
            {'result': 0.123, 'doc_id': '5bea4d3efa3646879'}
    """
    data = json.loads(request.get_data())
    account1 = data['account1']
    account2 = data['account2']
    score = query_existing_similarity_in_db(account1, account2)
    if len(score) == 0:
        try:
            info1 = retrieve(account1, mode=REALTIME_MODE)
            info2 = retrieve(account2, mode=REALTIME_MODE)
            vector = algoModule.calc(info1, info2, enable_networking=(account1['platform'] == account2['platform']),
                                     mode=REALTIME_MODE)
            doc_id = algoModule.store_result(info1, info2, vector, DATABASE_DATA_AWAIT_BATCH)
            score = Couch(DATABASE_DATA_AWAIT_BATCH).query({'_id': doc_id})
        except Exception as e:
            return make_response({'error': True, 'error_message': str(e)})
    doc = score[0]
    doc_id = doc['_id']
    vector = doc['vector']
    # todo: replace with machine learning overall score
    overall_score = 0.7573
    return make_response({'result': vector, 'columns': column_names,
                          'score': overall_score, 'doc_id': doc_id,
                          'error': False})


@app.route('/feedback', methods=["POST"])
def feedback():
    """
        Request format:
            {'doc_id': '5bea4d3efa3646879', 'feedback': 0}
            feedback: actual label.
                0: not same user
                1: same user
        Response format:
            {'result': 'ok'}
    """
    data = json.loads(request.get_data())
    db = Couch(DATABASE_FEEDBACK)
    db.insert(data)
    db.close()
    return make_response({'result': 'ok'})


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
