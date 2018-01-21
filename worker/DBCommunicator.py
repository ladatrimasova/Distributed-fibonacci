import MySQLdb


class DBCommunicator:
    host = 'localhost'
    DATABASE = 'test'
    TABLE_NAME = 'test2'
    USER = 'root'
    PASSWD = '342'
    HOST = 'DB'
    PORT = '3306'

    def __init__(self):
        self.create_table_if_not_exists()

    def connect(self):
        return MySQLdb.connect(host=self.DB, database=self.DATABASE, user=self.USER, passwd=self.PASSWD, port=self.PORT)

    def execute_update_query(self, query):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception:
            conn.rollback()

    def execute_select_query(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def create_table_if_not_exists(self):

        create_table_command = '''CREATE TABLE IF NOT EXISTS {} (
                 user_id INT PRIMARY KEY,
                 fib_number INT DEFAULT 0,
                 fib_value INT DEFAULT 0
             )'''.format(self.TABLE_NAME)

        self.execute_update_query(create_table_command)

    def get_user_fib_value(self, user_id):
        select_query = "select fib_number, fib_value from {} where user_id={}".format(self.TABLE_NAME, user_id)
        return self.execute_select_query(select_query)[0]

    def set_user_fib_value(self, user_id, fib_number, fib_value):
        select_query = "update {} SET fib_number = {}, fib_value = {} where user_id={}".format(self.TABLE_NAME,
                                                                                               fib_number, fib_value,
                                                                                               user_id)
        self.execute_update_query(select_query)

    def insert_new_user_if_not_exists(self, user_id, default_fib_number, default_fib_value):
        insert_user_query = "insert into {0} SELECT {1}, {2}, {3} WHERE NOT EXISTS (select * from {0} where user_id={1});".format(
            self.TABLE_NAME, user_id, default_fib_number, default_fib_value)
        self.execute_update_query(insert_user_query)
