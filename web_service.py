from flask import Flask, request
from flask_cors import CORS
import sys
from api import elastic_search
from elasticsearch import Elasticsearch
from flask import jsonify
import urllib3
app = Flask(__name__)
CORS(app)

@app.route('/validate',methods=['POST'])
def get_data():
    try:
        es = Elasticsearch(
            ["10.142.0.2", "10.142.0.3", "10.160.0.2"],
            scheme="http",
            port=9200,
        )
    except urllib3.exceptions.ConnectTimeoutError:
        print('connection timeout issue, check the server ip"s are correct.')
    name = 'test_cases'
    tc = elastic_search.TestCases(es)
    if(len(request.form['query'].split()) > 1):
        result = tc.match_search(name, request.form['query'])
    else:
        if('-' in request.form['query']):
            result = tc.match_phrase_search(name, request.form['query'])
        else:
            result = tc.match_term_search(name, request.form['query'])
    app.logger.info(request.form['query'])
    app.logger.info(result)
    return jsonify(result)

if __name__ == '__main__':
   app.run(host= '0.0.0.0', debug=True)