from .models import Gist
import sqlite3
from datetime import datetime


def search_gists(db_connection, **kwargs):
    # Call helper function to create a search query for passed args
    query = build_query(**kwargs)
    # Call search query
    cursor = db_connection.execute(query)
    # For each record in query response yield Gist created from data
    for row in cursor:
        yield Gist(row)

def build_query(**kwargs):
    # This function takes all key word argument pairs and builds a query from
    #  them to get appropriate gists data
    # Assumptions:
    # - datetime is only passed with keys in format of: column_name__op
    # - Only supports op of: lt, lte, gt, gte
    
    # Basic query so that if no arguments returns all records
    query = """select * from gists
    where 1=1
    """
    
    # Dictionary to convert key to operator
    op_dict = {
        'gt': ">",
        'gte': '>=',
        'lt': '<',
        'lte': '<='
    }
    
    # loop through each key and value passed
    for key, val in kwargs.items():
        # If dealing with a datetime need to handle specially
        if isinstance(val,datetime):
            # if the last letter is e then the operator is 3 letters instead of 2
            ii = -1 if key[-1:] == 'e' else 0
            # Parse operator from the key
            operator = op_dict[key[-2+ii:]]
            # Parse the field name from the key
            field = key[0:-4+ii]
            # Append to the query a new line: and datetime(field) operator datetime(value)
            query = query + "and datetime({}) {} datetime('{}')\n".format(field, operator, val)
        else:
            # If the value is a string need to add quotes for SQL
            val = "'{}'".format(val) if isinstance(val, str) else val
            # Append to the query a new line: and field = value
            query = query + 'and {} = {}\n'.format(key, val)
    
    return query
