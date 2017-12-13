import requests
import sqlite3
import os
from os.path import dirname as dot

BASE_PROJECT_PATH = dot(dot(__file__))
DATABASE_SCHEMA_PATH = os.path.join(BASE_PROJECT_PATH, 'schema.sql')

API_ENDPOINT = 'https://api.github.com'

INSERT_QUERY = """
    INSERT INTO gists 
    (github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url,
     public, created_at, updated_at, comments, comments_url)
    VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url,
     :forks_url, :public, :created_at, :updated_at,:comments, :comments_url);
"""


def import_gists_to_database(db, username, commit=True):
    USER_GIST_URL = 'https://api.github.com/users/{username}/gists'.format(username=username)

    r = requests.get(USER_GIST_URL)
    r.raise_for_status()

    r = r.json()

    for data in r:
        fields = {
            'github_id': data['id'], 'html_url': data['html_url'],
            'git_pull_url': data['git_pull_url'], 'git_push_url': data['git_push_url'],
            'commits_url': data['commits_url'], 'forks_url': data['forks_url'],
            'public': data['public'], 'created_at': data['created_at'],
            'updated_at': data['updated_at'], 'comments': data['comments'],
            'comments_url': data['comments_url'],
        }
        cursor = db.execute(INSERT_QUERY, fields)

    if commit:
        db.commit()


if __name__ == '__main__':
    with sqlite3.connect("gists.sqlite") as db:
        import_gists_to_database(db, "AllenAnthes", True)

