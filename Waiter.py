# -*- coding: GBK -*-
from flask import request, redirect, url_for, send_from_directory, render_template,session,escape
from __init__ import app
from sqlHelper import sqlhelper


@app.route('/waiterLogin', methods=['GET', 'POST'])
def waiterLogin():
    if request.method == 'GET':
        return render_template('waiterLogin.html')
    Rresult = sqlhelper.select_excution('''
        select * from Rtable where Tid = %s;
    ''' % request.form['Tid'])
    Wresult = sqlhelper.select_excution('''
        select * from Waiter where Wnum = '%s';
    '''% request.form['Wnum'])
    if(len(Rresult)!=1 or len(Wresult)!=1):
        return """
        <script>
            alert('不存在桌号或工号');
            history.go(-1);
        </script>
        """
    session.pop('menu', None)
    session['menu']=menu(request.form['Tid'],request.form['Wnum'])
    #get session
    emenu= escape(session['menu'])

class menu(object):
    def __init__(self, Tid , Wnum):
        self.Tid = Tid
        self.Wnum = Wnum
        self.dishes = []


class dish(object):
    def __init__(self, Did, Dname, Dprice):
        self.Did = Did
        self.Dname = Dname
        self.Dprice = Dprice
