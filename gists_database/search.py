from .models import Gist
import sqlite3
from datetime import datetime

def search_gists(db_connection, **kwargs):
    query = build_query(**kwargs)
        
    cursor = db_connection.execute(query)
    for row in cursor:
        yield Gist(row)

def build_query(**kwargs):
    query = """select * from gists
    where 1=1
    """
    
    op_dict = {
        'gt': ">",
        'gte': '>=',
        'lt': '<',
        'lte': '<='
    }
    
    for key, val in kwargs.items():
        if isinstance(val,datetime):
            op = key[-3:] if key[-1:] == 'e' else key[-2:]
            field = key[0:-5] if key[-1:] == 'e' else key[0:-4]
            operator = op_dict[op]
            query = query + "and datetime({}) {} datetime('{}')\n".format(field, operator, val)
        else:
            if isinstance(val, str):
                val = "'{}'".format(val)
            query = query + 'and {} = {}\n'.format(key, val)
    
    return query
