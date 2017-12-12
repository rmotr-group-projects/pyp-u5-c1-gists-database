import requests
import sqlite3
from pprint import pprint
import os
from os.path import dirname as dot
from gists_database.models import Gist
from github import Github

BASE_PROJECT_PATH = dot(dot(__file__))
DATABASE_SCHEMA_PATH = os.path.join(BASE_PROJECT_PATH, 'schema.sql')

API_ENDPOINT = 'https://api.github.com'

INSERT_QUERY = """
INSERT INTO gists 
(github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url,
 public, created_at, updated_at, comments, commits_url)
VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url,
 :forks_url, :public, :created_at, :updated_at, :comments, :commits_url);
"""


def import_gists_to_database(db, username, commit=True):
    USER_GIST_URL = f'https://api.github.com/users/{username}/gists'

    with sqlite3.connect(db) as db:
        r = requests.get(USER_GIST_URL).json()

        for data in r:
            fields = {
                'github_id': data['id'], 'html_url': data['html_url'],
                'git_pull_url': data['git_pull_url'], 'git_push_url': data['git_push_url'],
                'commits_url': data['commits_url'], 'forks_url': data['forks_url'],
                'public': data['public'], 'created_at': data['created_at'],
                'updated_at': data['updated_at'], 'comments': data['comments'],
                'comments_url': data['comments_url'],
            }
            pprint(fields)
            # cursor = db.execute(INSERT_QUERY, fields)

        if commit:
            db.commit()


if __name__ == '__main__':
    import_gists_to_database("gists.sqlite", "AllenAnthes", True)

# fields = (index,
#           gist_data['id'], gist_data['html_url'], gist_data['git_pull_url'], gist_data['git_push_url'],
#           gist_data['commits_url'], gist_data['forks_url'], gist_data['public'], gist_data['created_at'],
#           gist_data['updated_at'], gist_data['comments'], gist_data['comments_url']
#           )
