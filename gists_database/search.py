from .models import Gist


def get_operator(operator_code):
    """
    Return the comparison operator based on string code in keyword argument
    """

    if operator_code == 'gt':
        return '>'

    elif operator_code == 'gte':
        return '>='

    elif operator_code == 'lt':
        return '<'

    return '<='


def where_statement(kwarg):
    """
    Return the where clause of the SQL query based on keyword given
    """

    if kwarg in ('github_id', 'public', 'comments'):
        return '{0} == :value_{0}'.format(kwarg)

    else:

        kwarg_split = kwarg.split('__')
        operator = get_operator(kwarg_split[1])
        return 'datetime({}) {} datetime(:date_{})'.format(kwarg_split[0], operator, kwarg)


def search_gists(db_connection, **kwargs):
    """
    Given database connection db_connection arbitrary keyword constraints,
    create a generator that yields the Gist object containing gist data
    """

    # initialize base query and params dictionary
    query = """SELECT * FROM gists WHERE {}"""
    params = {}

    # query if no keyword provided
    if not kwargs:

        query = "SELECT * FROM gists"
        cursor = db_connection.execute(query)

    # build conditional query given keyword arguments
    else:

        for count, kwarg in enumerate(kwargs):

            query = query.format(where_statement(kwarg))

            if count > 0:
                query += ' AND {}'.format(where_statement(kwarg))

            if kwarg in ('github_id', 'public', 'comments'):
                params['value_{}'.format(kwarg)] = kwargs[kwarg]
            else:
                params['date_{}'.format(kwarg)] = kwargs[kwarg]

        cursor = db_connection.execute(query, params)

    for gist in cursor:

        yield Gist(gist)
