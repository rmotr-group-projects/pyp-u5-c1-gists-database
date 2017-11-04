from .models import Gist


def search_gists(db_connection, **kwargs):
    
    op_dict = {"gt":">", "gte":">=", "lt": "<", "lte":"<=", "=": "="}
    search_query="SELECT * from gists"
    if kwargs:
        search_query+=" WHERE "
        multiple_search_cond = False
        for k, v in kwargs.items():
            attr, _, comparison_op = k.partition("__")
            if not comparison_op:
                comparison_op = "="
            if multiple_search_cond:
                search_query+=" AND "
            if attr in ("created_at", "updated_at"):
                search_query+="datetime(" + attr + ")" + op_dict[comparison_op] + "datetime('" + str(v) +"')"
            else:
                search_query+=attr + op_dict[comparison_op] + "'" + str(v) +"'"
            multiple_search_cond = True
                
            
        
    
    print(search_query)
    curs = db_connection.cursor()
    curs.execute(search_query)
    for res in curs:
        yield Gist(res)
