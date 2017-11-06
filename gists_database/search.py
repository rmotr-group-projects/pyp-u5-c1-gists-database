from .models import Gist
import sqlite3


def search_gists(db_connection, **kwargs):
    cursor = build_query(db_connection, **kwargs)
    for gist in cursor:
        yield Gist(gist)

def build_query(db, **kwargs):
    pre_query = ("SELECT * FROM gists")
    if kwargs:
        pre_query += ' WHERE'
    querylist = []
    for kwarg in kwargs:
        if kwarg[:10] =='created_at':
            time = kwargs[kwarg]
            search = " date(created_at) {} datetime('{}')"
            if kwarg == 'created_at__gt':
                op = '>'
                querylist.append (search.format(op, time))
            if kwarg =='created_at__gte':
                op = '>='
                querylist.append (search.format(op, time))
            if kwarg =='created_at__lt':
                op = '<'
                querylist.append (search.format(op, time))
            if kwarg =='created_at__lte':
                op = '<='
                querylist.append (search.format(op, time))
            #query = " WHERE date(created_at) {} datetime('{}')".format(op,
            #  time)
        if kwarg == 'github_id':
            querylist.append(" github_id = '{}'".format(kwargs[kwarg]))

    query = pre_query + ' AND'.join(querylist)
    return db.execute(query)

