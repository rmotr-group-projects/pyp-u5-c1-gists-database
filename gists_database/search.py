from models import Gist


def search_gists(db_connection, **kwargs):
    if len(kwargs) == 0:
        cur = db_connection.cursor()
        cur.execute('SELECT * FROM gists')
        for row in cur:
             yield Gist(row)
         
