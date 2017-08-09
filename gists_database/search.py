from .models import Gist
from datetime import datetime

def search_gists(db_connection, **kwargs):
    
    query, params = build_query(**kwargs)
    
    
    cursor = db_connection.execute(query, params)
    
    rtn = rtn_iter()
    
    for row in cursor:
        rtn.add(row)

    return rtn
    

def build_query(**kwargs):
    if not kwargs:
        query_str = "SELECT * FROM gists"
        params = {}
        return query_str, params
    else:
        query_str = "SELECT * FROM gists WHERE "
        #counter = 0
        filters = []
        params = {}
        
        for key, value in kwargs.items():
            if _is_date_query(key):
                new_key, op = key.split('__')
                operator = decode_op(op)
                filters.append('datetime(%s) {} datetime(:%s)'.format(operator) %(new_key, new_key))
                params[new_key] = value
            else:
                filters.append('%s = :%s' %(key, key))
                params[key] = value

            
            """if counter == 0:
                query_str += " {} = '{}'".format(key, value)
                counter += 1
            else:
                query_str += " AND {} = '{}'".format(key, value)
                counter += 1"""
                
        query_str += ' AND '.join(filters)
        
        return query_str, params
        
        
#  *Remember, the search should return an iterator that pumps out `Gist` objects (`Gist` definition is in `models.py`)*           


def decode_op(op):
    if op == 'gt':
        return '>'
    elif op == 'gte':
        return '>='
    elif op == 'lt':
        return '<'
    elif op == 'lte':
        return '<='
    else:
        raise ValueError()

def _is_date_query(query):
    if 'at' in query:
        return True
    return False
        
        
class rtn_iter(object):
    def __init__(self):
        self.gists = []
        self.index = 0
        
    
    def __iter__(self):
        self.index = 0
        return self
        
    def __next__(self):
        var = self.index
        self.index += 1
        if var > len(self.gists) - 1:
            raise StopIteration
        
        return Gist(self.gists[var])
        
    next = __next__
    
    def add(self, gist):
        self.gists.append(gist)
    
    def all(self):
        pass
        
    

