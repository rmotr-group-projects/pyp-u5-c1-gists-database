import requests
import sqlite3
import json





def import_gists_to_database(db, username, commit=True):
    r = requests.get('https://api.github.com/users/{}/gists'.format(username)) 
    if r.status_code != 200:
        raise requests.HTTPError()
        
    request_data = r.json()   #convert request data into json format
    
      #create db connetion
    
    for gist in request_data:
        
        github_id = gist["id"]
        html_url = gist["html_url"]
        git_pull_url = gist["git_pull_url"]
        git_push_url =gist["git_push_url"]
        commits_url =gist["commits_url"]
        forks_url =gist["forks_url"]
        public =gist["public"]
        created_at =gist["created_at"]
        updated_at =gist["updated_at"]
        comments = gist["comments"]
        comments_url = gist["comments_url"]
        
        query = """INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url, public,
        created_at, updated_at, comments, comments_url) VALUES (:github_id, :html_url, :git_pull_url, :git_push_url, 
        :commits_url, :forks_url, :public, :created_at, :updated_at, :comments, :comments_url)"""
        
        cursor = db.execute(query,
        {'github_id': github_id, 'html_url': html_url, 'git_pull_url': git_pull_url,
        'git_push_url': git_push_url, 'commits_url': commits_url, 'forks_url': forks_url, 
        'public': public, 'created_at': created_at, 'updated_at': updated_at, 'comments': comments, 
        'comments_url': comments_url}
        )
    
  


