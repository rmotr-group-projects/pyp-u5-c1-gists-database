import requests
import os
from os.path import dirname as dot

BASE_PROJECT_PATH = dot(dot(__file__))
DATABASE_SCHEMA_PATH = os.path.join(BASE_PROJECT_PATH, 'schema.sql')


INSERT_QUERY = """
    INSERT INTO gists 
    (github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url,
     public, created_at, updated_at, comments, comments_url)
    VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url,
     :forks_url, :public, :created_at, :updated_at,:comments, :comments_url);
"""


def import_gists_to_database(db, username, commit=True):
    user_gist_url = 'https://api.github.com/users/{username}/gists'.format(username=username)

    r = requests.get(user_gist_url)
    r.raise_for_status()

    # r = r.json()

    for data in r.json():
        fields = {
            'github_id': data['id'], 'html_url': data['html_url'],
            'git_pull_url': data['git_pull_url'], 'git_push_url': data['git_push_url'],
            'commits_url': data['commits_url'], 'forks_url': data['forks_url'],
            'public': data['public'], 'created_at': data['created_at'],
            'updated_at': data['updated_at'], 'comments': data['comments'],
            'comments_url': data['comments_url'],
        }
        db.execute(INSERT_QUERY, fields)

    if commit:
        db.commit()