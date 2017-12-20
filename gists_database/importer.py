import requests
import sqlite3
import pprint
from .models import Gist

def import_gists_to_database(db, username, commit=True):
    clear_table = """DELETE FROM gists;
                     DELETE from sqlite_sequence where name= 'gists' ;"""
    db.executescript(clear_table)
    if commit:
        db.commit()
    r = requests.get('https://api.github.com/users/%s/gists' % username)
    
    if r.status_code != 200:
        #r.raise_for_status()
        raise requests.exceptions.HTTPError
        
    query = """INSERT INTO gists (github_id,html_url,git_pull_url,git_push_url,commits_url,forks_url,public,created_at,updated_at,comments,comments_url) 
            VALUES (:id,:html_url,:git_pull_url,:git_push_url,:commits_url,:forks_url,:public,:created_at,:updated_at,:comments,:comments_url        
            );"""

    for dict in r.json():
        sub_dict = {key:dict[key] for key in ('id','html_url','git_pull_url','git_push_url','commits_url','forks_url', 'public','created_at','updated_at','comments','comments_url') if key in dict}
        #print(sub_dict)
        db.execute(query, sub_dict)
    if commit:
        db.commit()    
        

# #pprint.pprint(json_file[0]['id'])
# db = sqlite3.connect('schema.db')
# username = 'gvanrossum'
# import_gists_to_database(db, username)
# cursor = db.cursor()
# results = db.execute('SELECT * FROM gists')
# print("gists:")
# #print(results.fetchone())
# for row in results:
#     print row



