from models import Gist


def search_gists(db_connection, **kwargs):

    COMPARISON_OPERATORS = {
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<='
    }

    query = 'SELECT * from gists'
    cur = db_connection.cursor()
    values = []
    if len(kwargs) > 0:
        query += ' WHERE '
    for key, value in kwargs.items():
        if 'github_id' in kwargs:
            values.append(value)
            query += 'github_id = ?'
            if len(kwargs) > 1:
                query += ' AND '
        if 'created_at__' in key:
            operator = COMPARISON_OPERATORS[key.split('__')[1]]
            values.append(value)
            query += ' created_at {} ?'.format(operator)

    cur.execute(query, tuple(values))

    for row in cur:
        yield Gist(row)
