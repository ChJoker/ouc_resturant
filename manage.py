# -*- coding: GBK -*-
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from __init__ import app
from sqlHelper import sqlhelper
import uuid

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template('menu.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    return render_template('dish_list.html', dishes=sqlhelper.select_excution('''
        select Did,Sname,Dname,Dpice from dish LEFT JOIN Sort ON  dish.Soid=Sort.Soid;
    '''))


@app.route('/deldish/<Did>')
def delet_dish(Did):
    result = sqlhelper.insert_or_delet('''
        delete from dish where Did = %s;
   ''' % Did)
    return str(result)


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'GET':
        return render_template('add_dish.html', sorts=sqlhelper.select_excution('''
            select Soid,Sname from Sort;
        '''))
    file = request.files['picture']
    if file and allowed_file(file.filename):
        savefile = str(uuid.uuid1()) + '.' + file.filename.rsplit('.', 1)[1];
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], savefile))
    result = sqlhelper.insert_or_delet("""
        insert into dish (Soid,Dname,Dpice,Dpic) values (%s,N'%s',%f,'%s');
    """ % (request.form['Soid'], request.form['Dname'], float(request.form['Dpice']), savefile))
    return redirect(url_for('dishes'))


@app.route('/add_sort', methods=['GET', 'POST'])
def add_sort():
    if request.method == 'GET':
        return render_template('add_sort.html', sorts=sqlhelper.select_excution('''
            select Soid,Sname from Sort;
        '''))
    result = sqlhelper.insert_or_delet("""
        insert into Sort (Sname) values (N'%s');
    """ % (request.form['Sname']))
    return redirect(url_for('add_sort'))


@app.route('/delet_sort/<delet_id>')
def delet_sort(delet_id):
    result = sqlhelper.insert_or_delet("""
        delete from Sort where Soid=%s;
    """ % (delet_id))
    return redirect(url_for('add_sort'))


@app.route('/cookers', methods=['GET', 'POST'])
def cookers():
    return render_template('cookers.html', cookers=sqlhelper.select_excution('''
        select Cid,Sname,Cnum,Cname,Cage,Csex from Cook LEFT JOIN Sort ON  Cook.Soid=Sort.Soid;
    '''))


@app.route('/delcook/<Cid>')
def delcook(Cid):
    result = sqlhelper.insert_or_delet('''
        delete from Cook where Cid = %s;
   ''' % Cid)
    return str(result)


@app.route('/add_cook', methods=['GET', 'POST'])
def add_cook():
    if request.method == 'GET':
        return render_template('add_cook.html', sorts=sqlhelper.select_excution('''
            select Soid,Sname from Sort;
        '''))
    result = sqlhelper.insert_or_delet("""
        insert into cook (Soid,Cname,Cage,Csex) values (%s,N'%s',%s,N'%s');
    """ % (request.form['Soid'], request.form['Cname'], request.form['Cage'], request.form['Csex']))
    return redirect(url_for('cookers'))


@app.route('/waiters', methods=['GET', 'POST'])
def waiters():
    return render_template('waiters.html', waiters=sqlhelper.select_excution('''
        select Wid,Wnum,Wname,Wage,wsex,Wroom from Waiter;
    '''))


@app.route('/delwaiter/<Wid>')
def delwaiter(Wid):
    result = sqlhelper.insert_or_delet('''
        delete from Waiter where Wid = %s;
   ''' % Wid)
    return str(result)


@app.route('/add_waiter', methods=['GET', 'POST'])
def add_waiter():
    if request.method == 'GET':
        return render_template('add_waiter.html', Rooms=sqlhelper.select_excution("""
            select Tname from Rtable where Tname!=N'大厅';
        """))
    result = sqlhelper.insert_or_delet("""
        insert into Waiter (Wname,Wage,wsex,Wroom) values (N'%s',%s,N'%s',N'%s');
    """ % (request.form['Wname'], request.form['Wage'], request.form['wsex'], request.form['Wroom']))
    return redirect(url_for('waiters'))


@app.route('/add_hallTable', methods=['GET', 'POST'])
def add_hallTable():
    if request.method == 'GET':
        return render_template('add_hallTable.html', Tables=sqlhelper.select_excution("""
            select Tsize,Tid from Rtable where Tname=N'大厅';
        """))
    result = sqlhelper.insert_or_delet("""
        insert into Rtable (Tsize,Tstate,Tname) values (%d,0,N'大厅');
    """ % int(request.form['Tsize']))
    return redirect(url_for('add_hallTable'))


@app.route('/add_roomTable', methods=['GET', 'POST'])
def add_roomTable():
    if request.method == 'GET':
        return render_template('add_roomTable.html', Tables=sqlhelper.select_excution("""
            select Tname,Tsize,Tid from Rtable where Tname!=N'大厅';
        """))
    result = sqlhelper.insert_or_delet("""
        insert into Rtable (Tsize,Tstate,Tname) values (%s,0,N'%s');
    """ % (request.form['Tsize'], request.form['Tname']))
    return redirect(url_for('add_roomTable'))


@app.route('/deltable/<Tid>')
def deltable(Tid):
    result = sqlhelper.insert_or_delet("""
        delete from Rtable where Tid=%s;
    """ % Tid)
    return str(result)
