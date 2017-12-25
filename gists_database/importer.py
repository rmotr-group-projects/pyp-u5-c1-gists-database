import requests
import sqlite3
from .models import Gist


def import_gists_to_database(db, username, commit=True):
    r = requests.get('https://api.github.com/users/%s/gists' % username)
    r.raise_for_status()
    
    query = "INSERT INTO gists (github_id,html_url,git_pull_url,git_push_url,\
        commits_url,forks_url,public,created_at,updated_at,comments,comments_url)\
        VALUES (:github_id,:html_url,:git_pull_url,:git_push_url,:commits_url,\
        :forks_url,:public,:created_at,:updated_at,:comments,:comments_url)"
    
    for data in r.json():
        db.execute(query, {
           'github_id': data['id'],
           'html_url': data['html_url'],
           'git_pull_url': data['git_pull_url'],
           'git_push_url': data['git_push_url'],
           'commits_url': data['commits_url'],
           'forks_url': data['forks_url'],
           'public': data['public'],
           'created_at': data['created_at'],
           'updated_at': data['updated_at'],
           'comments': data['comments'],
           'comments_url': data['comments_url']
           })
    
    if commit:
        db.commit()
    