import pyodbc
from __init__ import app

cnxn = pyodbc.connect(app.config['SQL_CONNECTSTRING'])
curson = cnxn.cursor()

row = curson.execute("insert into bill ( Bsun,Bstate) values (12,0);")
seed_id=curson.execute('SELECT SCOPE_IDENTITY(); ').fetchone()
print(seed_id[0])

# for row in curson.execute("select * from sort where Soid = ? ", 1):
#   print 'the id is %d , and type name is %s' % (row[0], row.Sname)

#
# for row in rows:
#     print 'the id is %d , and type name is %s' % (row[0], row.Sname)
cnxn.close()