# -*- coding: GBK -*-
from flask import request, redirect, url_for, send_from_directory, render_template
from __init__ import app
from sqlHelper import sqlhelper

@app.route('/select_hall')
def select_hall():
    return render_template('select_hall.html',tabless=sqlhelper.select_excution("""
        select Tid,Tsize,Tstate from Rtable where Tname = N'大厅';
    """))

@app.route('/select_hall/<int:where>/<Tid>')
def select_table(Tid,where):
    result = sqlhelper.insert_or_delet("""
        update Rtable set Tstate = 1 where Tid=%s;
    """ % Tid)
    if(where==0):
        return redirect(url_for('select_hall'))
    else:
        return redirect(url_for('select_room'))

@app.route('/select_room')
def select_room():
    return render_template('select_room.html',tables=sqlhelper.select_excution("""
        select Tid,Tsize,Tstate,Tname from Rtable where Tname != N'大厅';
    """))

