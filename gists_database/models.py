class Gist(object):
    def __init__(self, gist):
        self.id = gist[0]
        self.github_id = gist[1]
        self.html_url = gist[2]
        self.git_pull_url = gist[3]
        self.git_push_url = gist[4]
        self.commits_url = gist[5]
        self.forks_url = gist[6]
        self.public = gist[7]
        self.created_at = gist[8]
        self.updated_at = gist[9]
        self.comments = gist[10]
        self.comments_url = gist[11]

    def __str__(self):
        return 'Gist: {}'.format(self.github_id)


g = [{'comments': 0,
      'comments_url': 'https://api.github.com/gists/fc6fd66802cf326a6fa83b1d64123170/comments',
      'commits_url': 'https://api.github.com/gists/fc6fd66802cf326a6fa83b1d64123170/commits',
      'created_at': '2017-12-12T19:37:15Z',
      'description': 'Test Gist 1',
      'files': {'test.py': {'filename': 'test.py',
                            'language': 'Python',
                            'raw_url': 'https://gist.githubusercontent.com/AllenAnthes/fc6fd66802cf326a6fa83b1d64123170/raw/78376a31fb458ea3ddbc984aea1ed717f085884d/test.py',
                            'size': 28,
                            'type': 'application/x-python'}},
      'forks_url': 'https://api.github.com/gists/fc6fd66802cf326a6fa83b1d64123170/forks',
      'git_pull_url': 'https://gist.github.com/fc6fd66802cf326a6fa83b1d64123170.git',
      'git_push_url': 'https://gist.github.com/fc6fd66802cf326a6fa83b1d64123170.git',
      'html_url': 'https://gist.github.com/fc6fd66802cf326a6fa83b1d64123170',
      'id': 'fc6fd66802cf326a6fa83b1d64123170',
      'owner': {'avatar_url': 'https://avatars1.githubusercontent.com/u/27715246?v=4',
                'events_url': 'https://api.github.com/users/AllenAnthes/events{/privacy}',
                'followers_url': 'https://api.github.com/users/AllenAnthes/followers',
                'following_url': 'https://api.github.com/users/AllenAnthes/following{/other_user}',
                'gists_url': 'https://api.github.com/users/AllenAnthes/gists{/gist_id}',
                'gravatar_id': '',
                'html_url': 'https://github.com/AllenAnthes',
                'id': 27715246,
                'login': 'AllenAnthes',
                'organizations_url': 'https://api.github.com/users/AllenAnthes/orgs',
                'received_events_url': 'https://api.github.com/users/AllenAnthes/received_events',
                'repos_url': 'https://api.github.com/users/AllenAnthes/repos',
                'site_admin': False,
                'starred_url': 'https://api.github.com/users/AllenAnthes/starred{/owner}{/repo}',
                'subscriptions_url': 'https://api.github.com/users/AllenAnthes/subscriptions',
                'type': 'User',
                'url': 'https://api.github.com/users/AllenAnthes'},
      'public': True,
      'truncated': False,
      'updated_at': '2017-12-12T19:37:15Z',
      'url': 'https://api.github.com/gists/fc6fd66802cf326a6fa83b1d64123170',
      'user': None}]
