from models import Gist


def search_gists(db_connection, **kwargs):
    cur = db_connection.cursor()
    if len(kwargs) == 0:
        cur.execute('SELECT * FROM gists')
    elif 'github_id' in kwargs:
        cur.execute('SELECT * FROM gists WHERE github_id = :github_id',
        { 'github_id': kwargs.get('github_id') })
    
    for row in cur:
        yield Gist(row)