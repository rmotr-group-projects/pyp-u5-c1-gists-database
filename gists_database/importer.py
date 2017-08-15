import requests


def import_gists_to_database(db, username, commit=True):
    r = requests.get('https://api.github.com/users/{username}/gists'.format(username=username))
    if r.status_code == 200:
        query = "INSERT INTO gists (github_id, html_url,git_pull_url,git_push_url, commits_url, forks_url, \
            public, created_at, updated_at, comments, comments_url ) VALUES \
            (:github_id, :html_url, :git_pull_url, :git_push_url, :commits_url, :forks_url, \
                    :public, :created_at, :updated_at, :comments, :comments_url );"
        for element in r.json():
            cursors = db.execute(query,
                {'github_id':element.get('id'), 'html_url':element.get('html_url'), 'git_pull_url':element.get('git_pull_url'),\
                'git_push_url':element.get('git_push_url'), 'commits_url':element.get('commits_url'), 'forks_url':element.get('forks_url'), \
                'public':element.get('public'), 'created_at':element.get('created_at'), 'updated_at':element.get('updated_at'), \
                'comments':element.get('comments'), 'comments_url':element.get('comments_url')})

        db.commit()
    else:
        r.raise_for_status()

