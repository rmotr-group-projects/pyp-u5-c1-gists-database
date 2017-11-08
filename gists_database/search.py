from .models import Gist
import sqlite3

def search_gists(db_connection, **kwargs):
    conn = db_connection
    curs = conn.cursor()
    query = """SELECT * FROM gists;"""
    if kwargs:
        query = """SELECT * FROM gists WHERE ({});""".format(build_query(**kwargs))
    results = curs.execute(query, kwargs)
    for result in results:
        yield Gist(result)
        
def build_query(**kwargs):
    conditions = []
    key_condition = []
    comparisons = { 'gt'  : '>',
                    'gte' : '>=',
                    'lt'  : '<',
                    'lte' : '<='}
                    
    for condition in kwargs:
        key_condition = condition.split('__')
        if len(key_condition) > 1:
            conditions.append("""datetime({}) {} datetime(:{})""".format(key_condition[0],comparisons[key_condition[1]], condition))
        else:
            conditions.append('{} = :{}'.format(condition,condition))

    return ' and '.join(conditions)
