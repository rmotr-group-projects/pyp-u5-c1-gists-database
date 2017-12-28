from gists_database.models import Gist
from datetime import datetime
import requests


def import_gists_to_database(db, username, commit=True):
    """
    Uses the GitHub gists API to retrieve the gists of a given user, insert 
    those gists into a database (schema found in the schema.sql file), and if 
    commit is True, commits those changes to the database.
    """
    query = """
            INSERT INTO gists
                ('github_id', 'html_url', 'git_pull_url', 'git_push_url', 
                 'commits_url', 'forks_url', 'public', 'created_at', 
                 'updated_at', 'comments', 'comments_url')
            VALUES
                (:github_id, :html_url, :git_pull_url, :git_push_url, 
                :commits_url, :forks_url, :public, :created_at, :updated_at, 
                :comments, :comments_url);
            """

    r = requests.get('https://api.github.com/users/{username}/gists'.format(username=username))
    
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError("{}-doesnt-exist".format(username))
    
    json_data = r.json()
    
    for elem in json_data:
        # Grab certain information from the json data. This information will be 
        # inserted into the database.
        fields = {
            'github_id':    elem['id'],
            'html_url':     elem['html_url'],
            'git_pull_url': elem['git_pull_url'],
            'git_push_url': elem['git_push_url'],
            'commits_url':  elem['commits_url'],
            'forks_url':    elem['forks_url'],
            'public':       elem['public'],
            'created_at':   elem['created_at'],
            'updated_at':   elem['updated_at'],
            'comments':     elem['comments'],
            'comments_url': elem['comments_url']
        }
        
        cursor = db.execute(query, fields)

        if commit:
            db.commit()