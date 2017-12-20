import sqlite3
from .models import Gist
from datetime import datetime

filter_dict = {'github_id' : 'and github_id = :github_id',     
                'public' : 'and public = : public', 
                'created_at__gt':  'and datetime(substr(created_at,1,10)) > datetime(:created_at__gt)',
                'created_at__gte': 'and datetime(substr(created_at,1,10)) >= datetime(:created_at__gte)',
                'created_at__lt':  'and datetime(substr(created_at,1,10)) < datetime(:created_at__lt)',
                'created_at__lte': 'and datetime(created_at) <= datetime(:created_at__lte)',
                'updated_at__gt':  'and datetime(substr(updated_at,1,10)) > datetime(:updated_at__gt)', 
                'updated_at__gte': 'and datetime(updated_at) >= datetime(:updated_at__gte)',
                'updated_at__lt':  'and datetime(substr(updated_at,1,10)) < datetime(:updated_at__lt)',
                'updated_at__lte': 'and datetime(substr(updated_at,1,10)) <= datetime(:updated_at__lte)',
                'comments': 'and comments = :comments'}

def search_gists(db_connection, **kwargs):
    global filter_dict
    cursor = db_connection.cursor()
    query = """SELECT *  
                            FROM gists
                            WHERE 1 = 1 
                            """
    filter_str = ''
    for key in kwargs:
        if key in filter_dict:
            filter_str = filter_str + ' ' +filter_dict[key] 
            # print (filter_str)
    final_query = query + ' ' +filter_str
    print(final_query)
    print(kwargs)
    results = db_connection.execute(final_query, kwargs)  #{'created_at__gt': datetime(2017,5,10), 'created_at__gte': datetime(2017,5,10)})
    for gist in results:
        yield  Gist(gist)



#db = sqlite3.connect('schema.db')
# from tests.fixtures import populated_gists_database as db
# d = datetime(2014, 5, 3, 20, 26, 8)
# gists_iterator = search_gists(next(db()), created_at__lte=d, updated_at__gte=d)
# #gists_iterator = search_gists(next(db()), created_at__lte=d)
# gists = [g for g in iter(gists_iterator)]

# print(len(gists)) # == 1

# gist = gists[0]
# print(gist.github_id) # == '18bdf248a679155f1381'





