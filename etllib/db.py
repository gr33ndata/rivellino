import MySQLdb

class DB:

    def __init__(self, config=None):
        self.db=MySQLdb.connect(
            user=config['db_user'], 
            passwd=config['db_passwd'], 
            port=config['db_port'], 
            db=config['db_name'],
            host=config['db_host'])
        self.cursor=self.db.cursor()

    @classmethod
    def field_names(cls, cursor):
        if cursor.description:
            names = [item[0] for item in cursor.description]
        else:
            names = []
        return tuple(names)

    def cursor(self):
        return self.cursor

    def pages(self, data_len, page_size):
        return [ (i, min(i+page_size, data_len)) 
                for i in range(0, data_len, page_size)]

    def execute(self, sql=''):
        self.cursor.execute(sql)
        self.db.commit()

    def executemany(self, sql_str, values, page_size=1000):
        data_len = len(values)
        for i,j in self.pages(data_len, page_size):
            self.cursor.executemany(sql_str, values[i:j])
        self.db.commit()
