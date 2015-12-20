import pyodbc

cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=ouc_hotel;Trusted_Connection=yes;')
curson = cnxn.cursor()

for row in curson.execute("select * from sort where Soid = ? ", 1):
    print 'the id is %d , and type name is %s' % (row[0], row.Sname)
