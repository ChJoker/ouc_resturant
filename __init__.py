from flask import Flask
import os
import sys,logging

app = Flask(__name__)

#app.config['SQL_CONNECTSTRING'] = r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=ouc_hotel;Trusted_Connection=yes;'
app.config['SQL_CONNECTSTRING'] = r'Driver={SQL Server Native Client 11.0};Server=(localdb)\v11.0;Database=ouc_restaurant;Trusted_Connection=yes;'
app.config['UPLOAD_FOLDER'] = os.path.join(sys.path[0],'upload')
try:
    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER']))
except StandardError , e:
    pass
app.config['DISH_STATE']={'init':0,'doing':1,'done':2,'finish':3,'cancel':4}
app.config['CACHE']={}
app.secret_key = '12345678'
import manage
import Reception
import Waiter
import Cooker