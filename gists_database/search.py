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

    for i, (key, value) in enumerate(kwargs.items()):
        if key == 'github_id':
            query += 'github_id = ?'
        if 'created_at__' in key or 'updated_at__' in key:
            operator = COMPARISON_OPERATORS[key.split('__')[1]]
            date_type = key.split('__')[0]
            query += 'datetime({}) {} datetime(?)'.format(date_type, operator)

        values.append(value)
        if len(kwargs) > 1 and i < (len(kwargs) - 1):
            query += ' AND '
    print('query', query)
    cur.execute(query, tuple(values))

    for row in cur:
        yield Gist(row)
