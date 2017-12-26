import sqlite3
import requests
import json
from pprint import pprint

db = sqlite3.connect('gists')

def import_gists_to_database(db, username='martinzugnoni', commit=True):
    response = requests.get('https://api.github.com/users/{}/gists'.format(username))
    response.raise_for_status()
    
    for r in response.json():
        params = {
            'github_id': r['id'],
            'html_url': r['html_url'],
            'git_pull_url': r['git_pull_url'],
            'git_push_url': r['git_push_url'],
            'commits_url': r['commits_url'],
            'forks_url': r['forks_url'],
            'public': r['public'],
            'created_at': r['created_at'],
            'updated_at': r['updated_at'],
            'comments': r['comments'],
            'comments_url': r['comments_url']}

        db.execute("""INSERT INTO gists ("github_id", "html_url", 
                            "git_pull_url", "git_push_url", "commits_url",
                            "forks_url", "public", "created_at", "updated_at",
                            "comments", "comments_url") VALUES (:github_id,
                            :html_url, :git_pull_url, :git_push_url,
                            :commits_url, :forks_url, :public, :created_at,
                            :updated_at, :comments, :comments_url);""", params)
        if commit:
            db.commit()
