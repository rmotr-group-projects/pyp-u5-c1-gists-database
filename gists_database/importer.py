"""
Makes an API request to GitHub to collect information on user's
Gists and stores this in an SQLite3 database. Database schema is
set by schema.sql
"""
import requests


def import_gists_to_database(db, username, commit=True):

    # request gists info of username and parse json file
    URL = 'https://api.github.com/users/{}/gists'

    r = requests.get(URL.format(username))
    r.raise_for_status()

    # query to execute in order to insert data from api requests
    query = """INSERT INTO gists (
                github_id,
                html_url,
                git_pull_url,
                git_push_url,
                commits_url,
                forks_url,
                public,
                created_at,
                updated_at,
                comments,
                comments_url
                )
                VALUES (
                :github_id,
                :html_url,
                :git_pull_url,
                :git_push_url,
                :commits_url,
                :forks_url,
                :public,
                :created_at,
                :updated_at,
                :comments,
                :comments_url
                );"""

    # get list of gists
    for data in r.json():

        # execute query that insers contents of data into database
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
