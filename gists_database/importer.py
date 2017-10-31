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
    
    r = requests.get('https://api.github.com/users/{}/gists'.format(username))
    r.raise_for_status()
    all_gists = r.json()
    
    for gist in all_gists:
        db.execute(query, gist)

    if commit:
        db.commit()