import pyodbc
from __init__ import app


class SqlHelper(object):
    def __init__(self, con_str):
        self.cs = con_str

    def select_excution(self, sqlstr):
        conn = pyodbc.connect(self.cs)
        curser = conn.cursor()
        print(sqlstr)
        rows = curser.execute(sqlstr).fetchall()
        conn.close()
        return rows

    def insert_or_delet(self, sqlsrt):
        conn = pyodbc.connect(self.cs)
        curser = conn.cursor()
        print(sqlsrt)
        row = curser.execute(sqlsrt).rowcount
        conn.commit()
        conn.close()
        return row

    def insert_get_seed(self, sqlsrt):
        conn = pyodbc.connect(self.cs)
        curser = conn.cursor()
        row = curser.execute(sqlsrt).rowcount
        seed_id=curser.execute('SELECT SCOPE_IDENTITY(); ').fetchone()
        conn.commit()
        conn.close()
        return seed_id[0]


sqlhelper = SqlHelper(app.config['SQL_CONNECTSTRING'])
