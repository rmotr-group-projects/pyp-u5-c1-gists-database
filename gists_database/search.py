from .models import Gist
import sqlite3
from datetime import datetime

def search_gists(db_connection, **kwargs):
    
    
    
   
    # make filter for where clause
    #map parms passed in kwargs to keys in database by making a dictionary {parms: key+operation...}
    
    map_parms_to_dbkey ={'github_id':'github_id =',   'public': 'public =',
                         'created_at__gt': 'datetime(created_at) >', 'created_at__gte':'datetime(created_at) >=', 
                         'created_at__lt': 'datetime(created_at) <', 'created_at__lte':'datetime(created_at) <=',
                         'updated_at__gt': 'datetime(updated_at) >', 'updated_at__gte':'datetime(updated_at) >=', 
                         'updated_at__lt':'datetime(updated_at ) <', 'updated_at__lte':'datetime(updated_at) <= ',
                         'comments': 'comments ='}
    
    
    if kwargs :
        parms_value_dict={}
        list_for_where_clause = []
        for parms, value in kwargs.items():
           parms_to_key = ('{} :{}'.format(map_parms_to_dbkey[parms], parms))
           parms_value={parms : value}
           parms_value_dict.update(parms_value)
           list_for_where_clause.append(parms_to_key)

        filter=' AND '.join(list_for_where_clause)
    
        select = 'Select * FROM gists WHERE {}'.format(filter)
        
        cursor=db_connection.execute(select, parms_value_dict)
    else:
        select=  'Select * FROM gists'
        
        cursor=db_connection.execute(select)
        
    
    gists_found = cursor.fetchall()
    
    gists_list =[]
    for gists in gists_found:
        result= Gist(gists)
        gists_list.append(result)
    return gists_list
        
