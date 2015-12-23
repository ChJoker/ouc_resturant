from flask import request, redirect, url_for, send_from_directory, render_template
from __init__ import app
from sqlHelper import sqlhelper

@app.route('/select_hall')
def reception_seletable():
    return render_template('reception_seletable',tables=sqlhelper.select_excution("""
        select Tid,Tsize,Tstate from Rtable where
    """))