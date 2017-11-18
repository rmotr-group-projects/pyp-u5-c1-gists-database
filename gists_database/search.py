from .models import Gist
from datetime import datetime


def operator(op):
    d = {'gt': '>', 'gte': '>=', 'lt': '<', 'lte': '<='}
    if op in d:
        return d[op]
    return '=='


def search_gists(db_connection, **kwargs):
    global query
    QUERY_GIST = 'SELECT * FROM gists'
    
    attributes = ['created_at', 'updated_at', 'github_id']

    logic = ''
    string = ''
    
    if not kwargs:
        QUERY_GIST +=';'
    
    else:
        for key, value in kwargs.items():
            karg = key.split('__') 
            
            k = karg[0]
            
            op = karg[1] if len(karg) > 1 else ''
            
            string += logic
            
            if k in attributes:
                if string:
                    string += ' and '

                if not k.startswith('git'):
                    string += ' datetime({}) {} :{} '.format(k, operator(op), key)
                else:
                    string += ' {} {} :{} '.format(k, operator(op), key)

                
        QUERY_GIST += ' WHERE ' + string + ';'
            
            
    query = db_connection.execute(QUERY_GIST, kwargs)
    for row in query:
        yield Gist(row)



