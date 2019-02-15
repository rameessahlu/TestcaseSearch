from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pprint import pprint
import json

class TestCases:

    def __init__(self, es):
        self.es = es

    def create_indice(self, index_name):
        """creating an index"""
        print('Indice "test_cases" created!')
        self.es.indices.create(index=index_name, ignore=400)

    def create_tc_mapping(self):
        """if we are not satisfied with the auto mapping done by the elasticsearch"""
        self.es.indices.put_mapping(
            index= 'test_cases',
            doc_type= 'test_case',
            body={}
        )

    def check_index_existense(self, name):
        if self.es.indices.exists(index=name):
            return True
        return False

    def get_tc_mapping(self):
        result = self.es.indices.get_mapping(index='test_cases', doc_type='test_case')
        pprint(result)

    def delete_indice(self, name):
        self.es.indices.delete(index=name)

    def tc_insertion(self, file_name):
        #doc1 = {'id':1, 'name': '', 'designedBy': '', 'description': '', 'dependencies':'', 'data': '', 'exp_result': '', 'priority': '', 'steps': [] }
        #self.es.index(index='test_cases', doc_type='test_case', id=1, body=doc1)
        #res = self.es.get(index='test_cases', doc_type='test_case', id=1)
        #print(res['_source'])
        with open(file_name) as f:
            data = json.load(f)
            #pprint(data)
        helpers.bulk(self.es, data)

    def match_search(self, tc_index, tc_name_keyword):
        res = self.es.search(index=tc_index, body={'query':{'match': {'name': tc_name_keyword}} })
        return res

    def match_phrase_search(self, tc_index, tc_name_keyword):
        res = self.es.search(index=tc_index, body={'query':{'match_phrase': {'name': tc_name_keyword}} })
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

    def match_term_search(self, tc_index, tc_name_keyword):
        res = self.es.search(index=tc_index, body={'query':{'term': {'name': tc_name_keyword}}})
        return res