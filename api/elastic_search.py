from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pprint import pprint
import json

class TestCases:

    def __init__(self, es):
        self.es = es

    def create_indice(self):
        #creating an index
        print('Indice "test_cases" created!')
        self.es.indices.create(index='test_cases', ignore=400)

    def create_tc_mapping(self):
        #if we are not satisfied with the auto mapping done by the elasticsearch
        self.es.indices.put_mapping(
            index= 'test_cases',
            doc_type= 'test_case',
            body={}
        )

    def get_tc_mapping(self):
        result = self.es.indices.get_mapping(index='test_cases', doc_type='test_case')
        pprint(result)

    def delete_indice(self):
        self.es.indices.delete(index='test_cases')

    def tc_insertion(self, file_name):
        #doc1 = {'id':1, 'name': '', 'designedBy': '', 'description': '', 'dependencies':'', 'data': '', 'exp_result': '', 'priority': '', 'steps': [] }
        #self.es.index(index='test_cases', doc_type='test_case', id=1, body=doc1)
        #res = self.es.get(index='test_cases', doc_type='test_case', id=1)
        #print(res['_source'])
        with open(file_name) as f:
            data = json.load(f)
            #pprint(data)
        helpers.bulk(self.es, data)

    def match_search(self, tc_name_keyword):
        res = self.es.search(index='test_cases', body={'from': 0, 'size': 0, 'query':{'match': {'name': tc_name_keyword}} })
        return res

    def match_phrase_search(self, tc_name_keyword):
        res = self.es.search(index='test_cases', body={'from': 0, 'size': 0, 'query':{'match_phrase': {'name': tc_name_keyword}} })
        '''
        sample query
        'query': {
            'bool': {
                'must_not': {
                    'match_phrase': {
                        'name': 'He had'
                    }
                },
                'should': {
                        'name': tc_name_kw2
                },
                'must': {},
                'regexp': {},
            }
        }
        '''
        return res

    def match_term_search(self, tc_name_keyword):
        res = self.es.search(index='test_cases', body={'from': 0, 'size': 0, 'query':{'term': {'name': tc_name_keyword}} })
        return res

if __name__ == '__main__':
    es = Elasticsearch(
        ['', '', ''],
        scheme="http",
        port=9200,
    )
    tc = TestCases(es)
    #tc.delete_indice()
    #tc.create_indice()
    #tc.tc_insertion('data/test_cases.json')

    if not es.indices.exists(index='test_cases'):
        tc.create_indice()

    pprint(tc.es.search(index='test_cases',  doc_type='test_case',
    body={
        'from': 0,
        'size': 100,
        'query': {
            'match': { 'name': 'unplug'
                #'name': {
                    #'value': 'he-had'#, 'flags' : 'INTERSECTION|COMPLEMENT|EMPTY',
                    #'max_determinized_states': 20000
                 #}
             }
         }
    }))




    '''
    "bool": {
  "filter": {
    "exists": {
      "field": "field2"
    }
  }
}
'''
