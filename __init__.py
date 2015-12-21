from flask import Flask
import os

app = Flask(__name__)

app.config['SQL_CONNECTSTRING'] = r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=ouc_hotel;Trusted_Connection=yes;'
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/upload'

import hello
