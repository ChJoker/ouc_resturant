import pyodbc
from __init__ import app


class SqlHelper(object):
    def __init__(self, con_str):
        self.cs = con_str

    def select_excution(self, sqlstr):
        conn = pyodbc.connect(self.cs)
        curser = conn.cursor()
        rows = curser.execute(sqlstr).fetchall()
        conn.close()
        return rows

    def insert_or_delet(self, sqlsrt):
        conn = pyodbc.connect(self.cs)
        curser = conn.cursor()
        row = curser.execute(sqlsrt).rowcount
        conn.commit()
        conn.close()
        return row


sqlhelper = SqlHelper(app.config['SQL_CONNECTSTRING'])
