import pyodbc
from __init__ import app

cnxn = pyodbc.connect(app.config['SQL_CONNECTSTRING'])
curson = cnxn.cursor()

rows = curson.execute("select * from sort where Soid = ? ", 1).fetchall()

# for row in curson.execute("select * from sort where Soid = ? ", 1):
#   print 'the id is %d , and type name is %s' % (row[0], row.Sname)

cnxn.close()
for row in rows:
    print 'the id is %d , and type name is %s' % (row[0], row.Sname)
