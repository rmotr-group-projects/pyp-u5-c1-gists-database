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
    # Prefix for the query if there are no kwargs it returns all
    pre_query = ("SELECT * FROM gists")
    # Add a querylist to add multiple search parameters
    query_list = []
    # If there are kwargs append the WHERE to the pre_query
    if kwargs:
        pre_query += ' WHERE'
    # Check for search parameters in kwargs and add them to querylist
    for kwarg in kwargs:
        if kwarg.startswith(
                            'created_at') or kwarg.startswith(
                            'updated_at__gte'):
            time = kwargs[kwarg]
            search = " date(created_at) {} datetime('{}')"
            if kwarg == 'created_at__gt':
                op = '>'
                query_list.append(search.format(op, time))
            if kwarg == 'created_at__gte':
                op = '>='
                query_list.append(search.format(op, time))
            if kwarg == 'created_at__lt':
                op = '<'
                query_list.append(search.format(op, time))
            if kwarg == 'created_at__lte':
                op = '<='
                query_list.append(search.format(op, time))
            if kwarg == 'updated_at__gte':
                op = '>='
                query_list.append(" date(updated_at) {} datetime('{}')".format(
                                  op, time))
        else:
            query_list.append(" {} = '{}'".format(kwarg, kwargs[kwarg]))

    query = pre_query + ' AND'.join(query_list)
    return db.execute(query)
