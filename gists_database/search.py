import sqlite3

from gists_database.models import Gist

QUERY = "SELECT * FROM gists"

OPERATIONS = {
    'gt': '>',
    'gte': '>=',
    'lt': '<',
    'lte': '<=',
}


def search_gists(db_connection, **kwargs):
    db_connection.row_factory = sqlite3.Row
    query, params = build_query(**kwargs)
    results = db_connection.execute(query, params)
    for gist in results:
        yield Gist(gist)


def build_query(**kwargs):
    if not kwargs:
        return QUERY, {}
    params = {}
    args = []
    for key, value in kwargs.items():
        if key in ('github_id', 'public', 'comments'):
            args.append('{key} = :{key}'.format(key=key))
            params[key] = value
        else:
            attr, symbol = key.split('__')
            args.append(
                'datetime({attr}) {op} datetime(:{attr})'.format(attr=attr, op=OPERATIONS[symbol]))
            params[attr] = value
    return QUERY + " WHERE " + ' AND '.join(args), params
