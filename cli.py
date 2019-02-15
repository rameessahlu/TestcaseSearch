from api import elastic_search
from elasticsearch import Elasticsearch
import click
import urllib3

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug
    try:
        es = Elasticsearch(
            ["34.73.66.219", "34.73.48.191", "35.200.149.35"],
            scheme="http",
            port=9200,
        )
    except urllib3.exceptions.ConnectTimeoutError:
        click.echo('connection timeout issue, check the server ip"s are correct.')
    ctx.obj['tc'] = elastic_search.TestCases(es)

@cli.command()
@click.pass_context
@click.option('--name', default='test_cases', help='To create an elasticsearch index.')
def create_index(ctx, name):
    """Function for index creation"""
    ctx = ctx.obj['tc']
    if not ctx.check_index_existense(name):
        ctx.create_indice(name)
        click.echo('Index {} created.'.format(name))
    else:
        click.echo('Index {} already exists!'.format(name))

@cli.command()
@click.pass_context
@click.option('--name', default='test_cases', help='To delete a specific elasticsearch index.')
def delete_index(ctx, name):
    """Function for index deletion"""
    ctx = ctx.obj['tc']
    if ctx.check_index_existense(name):
        ctx.delete_indice(name)
        click.echo('Index {} deleted.'.format(name))
    else:
        click.echo('Index {} doesn\'t exists!'.format(name))

@cli.command()
@click.pass_context
@click.option('--doc', default='data/test_cases.json', help='To specify the doc object file')
def insert_docs(ctx, doc):
    """Function for bulk document insertion"""
    ctx = ctx.obj['tc']
    ctx.tc_insertion(doc)

@cli.command()
@click.pass_context
@click.option('--query', default='data/test_cases.json', help='To specify the query string')
@click.option('--name', default='test_cases', help='To specify a specific elasticsearch index to look at.')
def search(ctx, query, name):
    """Function for bulk document insertion"""
    ctx = ctx.obj['tc']
    click.echo('Query string is {}.'.format(query))
    if(len(query.split()) > 1):
        click.echo(ctx.match_search(name, query))
    else:
        if('-' in query):
            click.echo(ctx.match_phrase_search(name, query))
        else:
            click.echo(ctx.match_term_search(name, query))



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
