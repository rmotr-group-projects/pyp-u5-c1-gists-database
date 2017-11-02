import requests


API_ENDPOINT = 'https://api.github.com/users/{username}/gists'

INSERT_GIST_QUERY = """INSERT INTO gists (
    "github_id", "html_url", "git_pull_url",
    "git_push_url", "commits_url",
    "forks_url", "public", "created_at",
    "updated_at", "comment", "comments_url"
) Values (
    :github_id, :html_url, :git_pull_url,
    :git_push_url, :commits_url, :forks_url,
);"""


def import_gists_to_database(db, username, commit=True):
    gists_request = requests.get(API_ENDPOINT.format(username=username))
#    gists = gists_request.json()
#    db = sqlite3.connect(db)