from .models import Gist
import sqlite3
import re

def search_gists(db_connection, **kwargs):
    cursor = db_connection.cursor()
    query = "SELECT * FROM gists"
    
    params = {
        'github_id' : kwargs.get('github_id'),
        'public' : kwargs.get('public'),
        'created_at__gt' : kwargs.get('created_at__gt'),
        'created_at__gte' : kwargs.get('created_at__gte'),
        'created_at__lt' : kwargs.get('created_at__lt'),
        'created_at__lte' : kwargs.get('created_at__lte'),
        'updated_at__gt' : kwargs.get('updated_at__gt'),
        'updated_at__gte' : kwargs.get('updated_at__gte'),
        'updated_at__lt' : kwargs.get('updated_at__lt'),
        'updated_at__lte' : kwargs.get('updated_at__lte'),
        'comments' : kwargs.get('comments')
    }
    
    filtered_params = dict(filter(lambda item: item[1] is not None, params.items()))
    print(filtered_params)
    
    if filtered_params is not None:
        query += " WHERE"
        for key, value in filtered_params.items():
            operator = '='
            if re.findall('__gt$', key):
                operator = '>'
            elif re.findall('__gte$', key):
                operator = '>='
            elif re.findall('__lt$', key):
                operator = '<'
            elif re.findall('__lte$', key):
                operator = '<='
            if '__' in key:
                query += " datetime({}) {} :{} AND".format(key.split('__')[0], operator, key)
            else:
                query += " {} {} :{} AND".format(key.split('__')[0], operator, key)
        query = query[:-4]
        
    print(query)
    
    cursor = db_connection.execute(query, filtered_params)
 
    #rows = cur.fetchall()
 
    for row in cursor:
        yield Gist(row)
