import requests
import sqlite3

def import_gists_to_database(db, username, commit=True):
    query = """INSERT INTO gists (
    github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url, 
    public, created_at, updated_at, comments, comments_url
    ) VALUES (
    :id, :html_url, :git_pull_url, :git_push_url, :commits_url, :forks_url,
    :public, :created_at, :updated_at, :comments, :comments_url
    );"""
    
    # Get all gists for passed user
    r = requests.get('https://api.github.com/users/{}/gists'.format(username))
    # Raise error if fail to receive data for user
    r.raise_for_status()
    # Convert all gists to JSON
    all_gists = r.json()
    
    # Loop through individual gists
    for gist in all_gists:
        # Execute saved insert query to store each gist in the db passed
        db.execute(query, gist)

    # If passed value of commit is set to true commit inserts
    if commit:
        db.commit()