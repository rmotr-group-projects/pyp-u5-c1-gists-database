from .models import Gist
import sqlite3


def search_gists(db_connection, **kwargs):
    # Cursor going through the the database
    # Using build_query to filter out the proper gist from the database
    cursor = build_query(db_connection, **kwargs)
    # This is a generator that returns the gist as a Gist object
    for gist in cursor:
        yield Gist(gist)


def build_query(db, **kwargs):
    pre_query = ("SELECT * FROM gists")
    if kwargs:
        pre_query += ' WHERE'
    querylist = []
    for kwarg in kwargs:
        if kwarg[:10] == 'created_at':
            time = kwargs[kwarg]
            search = " date(created_at) {} datetime('{}')"
            if kwarg == 'created_at__gt':
                op = '>'
                querylist.append(search.format(op, time))
            if kwarg == 'created_at__gte':
                op = '>='
                querylist.append(search.format(op, time))
            if kwarg == 'created_at__lt':
                op = '<'
                querylist.append(search.format(op, time))
            if kwarg == 'created_at__lte':
                op = '<='
                querylist.append(search.format(op, time))
        if kwarg == 'github_id':
            querylist.append(" github_id = '{}'".format(kwargs[kwarg]))

    query = pre_query + ' AND'.join(querylist)
    return db.execute(query)
