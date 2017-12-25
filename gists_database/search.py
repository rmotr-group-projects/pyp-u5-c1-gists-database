from .models import Gist
from datetime import datetime


def search_gists(db_connection, **kwargs):
    dict = {"gt":">", "gte":">=", "lt":"<", "lte":"<=", "=":"="}
    search_query = "SELECT * FROM gists"
    
    if kwargs:
        search_query += " WHERE "
        more_cond = 0
        for k, v in kwargs.items():
            attr, _, comparison = k.partition("__")
            if more_cond > 0: #if non-first run over kwargs
                search_query += " AND "
            if attr in ("created_at", "updated_at"):
                search_query += "datetime(" + attr + ")" + dict[comparison] + "datetime('" + str(v) + "')"
            else:
                search_query += attr + " = " + "'" + str(v) + "'"
            if len(kwargs) > 1: more_cond += 1
    
    cur = db_connection.cursor()
    cur.execute(search_query)
    for result in cur:
        yield Gist(result)
