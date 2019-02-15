from api import elastic_search
from elasticsearch import Elasticsearch
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug
    es = Elasticsearch(
        ["34.73.194.102", "34.73.6.197", "35.200.149.35"],
        scheme="http",
        port=9200,
    )
    ctx.obj['tc'] = elastic_search.TestCases(es)

@cli.command()
@click.pass_context
@click.option('--name', default='test_cases', help='To create an elasticsearch index.')
def create_index(ctx, name):
    """Function for index creation"""
    ctx = ctx.obj['tc']
    if not ctx.check_index_existense(name):
        ctx.create_indice(name)
        print('Index {} created.'.format(name))
    else:
        print('Index {} already exists!'.format(name))

@cli.command()
@click.pass_context
@click.option('--name', default='test_cases', help='To delete a specific elasticsearch index.')
def delete_index(ctx, name):
    """Function for index deletion"""
    ctx = ctx.obj['tc']
    if ctx.check_index_existense(name):
        ctx.delete_indice(name)
        print('Index {} deleted.'.format(name))
    else:
        print('Index {} doesn\'t exists!'.format(name))

@cli.command()
@click.pass_context
@click.option('--doc', default='data/test_cases.json', help='To specify the doc object file')
def insert_docs(ctx, doc):
    """Function for bulk document insertion"""
    ctx = ctx.obj['tc']
    ctx.tc_insertion(doc)



if __name__ == '__main__':
    cli(obj={})

'''
    #pprint(tc.es.search(index='test_cases',  doc_type='test_case',
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
    "bool": {
  "filter": {
    "exists": {
      "field": "field2"
    }
  }
}
'''
