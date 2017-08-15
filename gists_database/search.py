from .models import Gist
from datetime import datetime
import datetime


def search_gists(db_connection, **kwargs):
    operations={'gt': ">", 'gte': ">=", "lt": "<", 'lte': "<="}
    c = db_connection.cursor()
    g_list=[]
    if kwargs:
        for k in kwargs:
            if k.find('created') > -1:
                symbol = operations[k.split('__')[1]]
                query_by = k.split('__')[0]
                d=kwargs[k]
                d=d.strftime("%Y-%m-%d")
                #
                #"SELECT * FROM gists WHERE {created_at} {symbol} '{date}';".format(created_at=query_by, symbol=symbol, date=d))

                #"SELECT * FROM gists WHERE created_at <= '2014-05-04';"
                if symbol == "<=":
                    d=kwargs[k]
                    d= d+datetime.timedelta(days=1)
                    d=d.strftime("%Y-%m-%d")
                c.execute("SELECT * FROM gists WHERE {created_at} {symbol} '{date}';".format(created_at=query_by, symbol=symbol, date=d))
                for element in c.fetchall():
                    g_list.append(Gist(element))
        if 'github_id' in kwargs:
            if not g_list:
                c.execute("SELECT * FROM gists WHERE github_id ='{id}'".format(id=kwargs['github_id'])+ ";")
                for e in c.fetchall():
                    g_list.append(Gist(e))
            else:
                return [g for g in g_list if g.github_id==kwargs['github_id']]
        return g_list

    else:
        c.execute('SELECT * FROM gists')
        return c.fetchall()

def build_query():
    pass      

