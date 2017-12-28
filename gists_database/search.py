from gists_database.models import Gist
# from models import Gist
from datetime import datetime
# import sqlite3
import functools

def check_input(function):
    """
    This decorator is used to check the input in search_gists(). It checks for 
    valid keyword arguments, redundant arguments, and proper input for the 
    'proper' parameter.
    """
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        valid_args_list = ['github_id', 'public', 'created_at__gt', 'created_at__gte', 
                          'created_at__lt', 'created_at__lte', 'updated_at__gt', 
                          'updated_at__gte', 'updated_at__lt', 'updated_at__lte', 
                          'comments']
                           
        # Check for valid keyword arguments
        for key in kwargs.keys():
            if key not in valid_args_list:
                raise ValueError("invalid keyword argument '{}'".format(key))
        
        # Check for redundant arguments. Such as having both 'created_at__gt' and 
        # 'created_at__gte' as arguments.
        if any(['created_at__gt' in kwargs.keys() and 'created_at__gte' in kwargs.keys(), 
                'created_at__lt' in kwargs.keys() and 'created_at__lte' in kwargs.keys(), 
                'updated_at__gt' in kwargs.keys() and 'updated_at__gte' in kwargs.keys(), 
                'updated_at__lt' in kwargs.keys() and 'updated_at__lte' in kwargs.keys()]):
            raise ValueError("redundant arguments for created or updated times.")
        
        # Check that the 'public' argument is 0, 1, True, or False
        # Note: sqlite stores boolean values as 0 or 1 (not True or False).
        if 'public' in kwargs.keys():
            try:
                kwargs['public'] = int(kwargs['public'])
                # Double check that the converted integer is 0 or 1
                if kwargs['public'] not in [0, 1]:
                    raise ValueError
            except ValueError:
                raise ValueError("'public' argument must be 0, 1, True, or False.")
                
        return function(*args, **kwargs)
        
    return wrapped


def add_criteria(key, criteria_dict, kwargs_dict, constrained_field):
    """
    Utility function used in get_criteria_dict() to help handle the various 
    versions of the 'created_at' and 'updated_at' key word arguments in 
    search_gists().
    """
    constraint_string = "'" + str(kwargs_dict[key]) + "'"
    statement_list = [constrained_field, None, constraint_string]
    if key.endswith('gt'):
        statement_list[1] = '_at > '
    elif key.endswith('gte'):
        statement_list[1] = '_at >= '
    elif key.endswith('lt'):
        statement_list[1] = '_at < '
    elif key.endswith('lte'):
        statement_list[1] = '_at <= '
    criteria_dict[key] = ''.join(statement_list)
    


def get_criteria_dict(kwargs_dict):
    """
    Returns a dictionary. The keys are the key word arguments provided in 
    search_gists(), and the values are a string that will be used in the sqlite 
    query pertaining to that key. This function is used in search_gists().
    """
    criteria_dict = {}
    for key in kwargs_dict:
        # If the key contains 'created' or 'updated', then special modifications 
        # need to be made. Otherwise, we can use a standard modification.
        if 'created' in key:
            add_criteria(key, criteria_dict, kwargs_dict, 'created')
        elif 'updated' in key:
            add_criteria(key, criteria_dict, kwargs_dict, 'updated')
        else:
            criteria_dict[key] = str(key) + ' = ' + "'" + str(kwargs_dict[key]) + "'"
    return criteria_dict
    

def get_query(criteria_dict, kwargs):
    """
    Returns a string. This string is the query that will be used in 
    search_gists().
    """
    query = """
            SELECT 
                id, github_id, html_url, git_pull_url, git_push_url, 
                commits_url, forks_url, public, created_at, 
                updated_at, comments, comments_url 
            FROM 
                gists;"""
                
    # If the criteria dict is empty, then the query does not need a WHERE clause.
    if not criteria_dict:
        return query
    
    # A certain operator is used in the WHERE clause depending on the key word 
    # argument provided on search_gists().
    ends_with_dict = {
        '_gt': '>',
        'gte': '>=',
        '_lt': '<',
        'lte': '<=',
    }
    
    query = query[:-1] + ' WHERE '
    
    # List will be used to join each string with ' AND ' for the WHERE clause.
    clause_list = []
    
    for key in kwargs:
        # If the last three characters of the key are in ends_with_dict, then 
        # we need to incorporate datetime() into the string and include the 
        # relevant operator (a value in ends_with_dict).
        if key[-3:] in ends_with_dict:
            statement = 'datetime(' + str(key[:7]) + '_at) ' + ends_with_dict[key[-3:]] + ' datetime(:' + str(key) + ')'
            clause_list.append(statement)
        else:
            clause_list.append(str(key) + ' = :' + str(key))
            
    clause_string = ' AND '.join(clause_list)
    query += clause_string + ';'

    return query
        

@check_input
def search_gists(db_connection, **kwargs):
    """
    Takes a db_connection parameter (the database connection), as well as a 
    variable number of keyword arguments to use in the search. Returns an 
    iterator that pumps out Gist objects with all the appropriate data filled 
    in.
    """
    criteria_dict = get_criteria_dict(kwargs)
    query = get_query(criteria_dict, kwargs)
    cursor = db_connection.execute(query, kwargs)
    
    for row in cursor:
        yield Gist(row)