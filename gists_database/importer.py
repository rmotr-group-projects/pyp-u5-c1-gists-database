# Code in this file is from class on 11/1/17
import requests
from requests import exceptions
from .config import TABLE_NAME

API_ENDPOINT = 'https://api.github.com/users/{username}/gists'

INSERT_GIST_QUERY = """INSERT INTO {table} (
    "github_id", "html_url", "git_pull_url",
    "git_push_url", "commits_url",
    "forks_url", "public", "created_at",
    "updated_at", "comments", "comments_url"
) VALUES (
    :github_id, :html_url, :git_pull_url,
    :git_push_url, :commits_url, :forks_url,
    :public, :created_at, :updated_at,
    :comments, :comments_url
);"""


def import_gists_to_database(db, username, commit=True):
    url = API_ENDPOINT.format(username=username)
    resp = requests.get(url)
    resp.raise_for_status()
    """
    if resp.status_code == 404:
        raise exceptions.HTTPError("User not found")
    """
    gists = resp.json()

    for gist in gists:
        params = {
            "github_id": gist['id'],
            "html_url": gist['html_url'],
            "git_pull_url": gist['git_pull_url'],
            "commits_url": gist['commits_url'],
            "forks_url": gist['forks_url'],
            "public": gist['public'],
            "created_at": gist['created_at'],
            "updated_at": gist['updated_at'],
            "comments": gist['comments'],
            "comments_url": gist['comments_url'],
        }
        db.execute(INSERT_GIST_QUERY, params)
        if commit:
            db.commit()
