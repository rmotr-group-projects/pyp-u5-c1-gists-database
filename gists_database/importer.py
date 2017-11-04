import requests
import sqlite3

INSERT = """INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, commits_url, 
forks_url, public, created_at, updated_at, comments, comments_url) VALUES  
(:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url, 
:forks_url, :public, :created_at, :updated_at, :comments, :comments_url)"""

REQUEST_URL="https://api.github.com/users/{username}/gists"

def import_gists_to_database(db, username, commit=True):
    response = requests.get(REQUEST_URL.format(username=username))
    response.raise_for_status()
    json = response.json()
    
    curs = db.cursor()
    for g in json:
        gist_params = {"url" : g["url"],
        "github_id" : g["id"], 
        "html_url" : g["html_url"], 
        "git_pull_url" : g["git_pull_url"],
        "git_push_url" : g["git_push_url"], 
        "commits_url" : g["commits_url"],
        "forks_url" : g["forks_url"],
        "public" : g["public"], 
        "created_at" : g["created_at"],
        "updated_at" : g["updated_at"],
        "comments" : g["comments"],
        "comments_url" : g["comments_url"]}
        curs.execute(INSERT, gist_params)
    db.commit()
