import requests
import sqlite3
import json


def import_gists_to_database(db, username, commit=True):

    url='https://api.github.com/users/{}/gists'.format(username)

    r = requests.get(url)
    r.raise_for_status()
    resp=r.json()     #list
    
    
   
    
    
    #get each gist as a dictionary from the list called resp. and populate db.
    for element in resp:
       
       dict_for_db_element = {}
    
       for key, value in element.items():
           
          keys_wanted = ('id', 'html_url', 'git_pull_url', 'git_push_url', 'commits_url', 'forks_url', 'public', 'created_at',
                         'updated_at', 'comments', 'comments_url')
                         
          json_dict = {db_key: element[db_key] for db_key in keys_wanted}
    
       dict_for_db_element.update(json_dict)
    
       db.execute("""INSERT INTO gists
                  (github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url, public, created_at, updated_at, comments, comments_url)
                  VALUES 
                  (:id, :html_url, :git_pull_url, :git_push_url, :commits_url, :forks_url, :public, 
                   :created_at, :updated_at,:comments, :comments_url)""", dict_for_db_element)
                   
     
    db.commit()
    
    
