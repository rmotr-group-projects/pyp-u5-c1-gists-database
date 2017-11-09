from models import Gist


def search_gists(db_connection, **kwargs):
    cur = db_connection.cursor()
    if len(kwargs) == 0:
        cur.execute('SELECT * FROM gists')
    elif 'github_id' in kwargs:
        cur.execute('SELECT * FROM gists WHERE github_id = :github_id',
        { 'github_id': kwargs.get('github_id') })
    elif 'created_at__gt' in kwargs:
        cur.execute('SELECT * FROM gists WHERE datetime(created_at) >'
                    'datetime(:date)', { 'date': kwargs.get('created_at__gt')})  
        
    for row in cur:
        yield Gist(row)