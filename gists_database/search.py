from .models import Gist

def search_gists(db_connection, **kwargs):
    query, params = build_query(**kwargs)
    
    cursor = db_connection.execute(query, params)
    for row in cursor:
        yield Gist(row)

def build_query(**kwargs):
    condition = []
    params = {}
    ops_dict = {
        'gt': '>',
        'lt': '<',
        'gte': '>=',
        'lte': '<='
    }
    
    for key, value in kwargs.iteritems():
        fields = key.split('__')
        if len(fields) > 1:
            ops = ops_dict.get(fields[1], "=")
            condition.append("datetime({}) {} :{}".format(fields[0], ops, fields[0]))
        else:
            ops = "="
            condition.append("{} {} :{}".format(fields[0], ops, fields[0]))
        
        params[fields[0]] = value
        
    query = "SELECT * FROM gists WHERE 1=1"
    if condition:
        query += " AND " + " AND ".join(condition)
    
    return query, params