from .models import Gist
from datetime import datetime

def search_gists(db_connection, **kwargs):
    dict = {"gt":">", "gte":">=", "lt": "<", "lte":"<=", "=": "="}
    search_query="SELECT * from gists"
    if kwargs:
        search_query+=" WHERE "
        multiple_search_cond = False
        for k, v in kwargs.items():
            attr, _, comparison = k.partition("__")
            if not comparison:
                comparison = "="
            if multiple_search_cond:
                search_query+=" AND "
            if attr in ("created_at", "updated_at"):
                search_query+="datetime(" + attr + ")" + dict[comparison] + "datetime('" + str(v) +"')"
            else:
                search_query+=attr + dict[comparison] + "'" + str(v) +"'"
            multiple_search_cond = True
            
    print(search_query)
    curs = db_connection.cursor()
    curs.execute(search_query)
    for res in curs:
        yield Gist(res)
