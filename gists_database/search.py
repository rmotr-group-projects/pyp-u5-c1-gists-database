from .models import Gist

# sql syntax example  
# d = datetime(2017, 5, 10)
# cursor = db.execute('SELECT * FROM gists WHERE created_at > datetime(:created_at)', {'created_at': d})

class search_gists(object):
    # parse key string to column and operator
    OPERATION_STRING = {
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>='
    }
    
    # datatime columns
    DATETIME_COLUMNS = ('created_at', 'updated_at')
    
    # parse string to column + operator
    def _parse(self, key_string):
        if '__' in key_string:
            column, op_string = key_string.split('__')
            op = self.__class__.OPERATION_STRING[op_string]
        else:
            column = key_string
            op = '='
        return column, op   
        
    # check if the column is datetime type. Datetime column has different sql syntax
    def is_datetime(self, column):
        if column in self.__class__.DATETIME_COLUMNS:
            return True
        return False
        
    # initialization, create the db cursor
    def __init__(self, db_connection, **kwargs):
        db_connection = db_connection
        query = 'SELECT * FROM gists'
        values = {}
        if kwargs:
            filters = []
            for key_string, value in kwargs.items():
                column, op = self._parse(key_string)
                
                if self.is_datetime(column):
                    filters.append('datetime(%s) %s datetime(:%s)' % (column, op, key_string))
                else :
                    filters.append('%s %s :%s' % (column, op, key_string))
                    
                values[key_string] = value

            query += ' WHERE '
            query += ' AND '.join(filters) 
        self.cursor =db_connection.execute(query, values)
        
    # iteratable
    def __iter__(self):
        return self
        
    # iterator
    def __next__(self):
        result = self.cursor.fetchone()
        if result is None:
            raise StopIteration()
        return Gist(result) 

    next = __next__ 
