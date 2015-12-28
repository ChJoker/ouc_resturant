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

@app.route('/display_bill')
def display_bill():
    bills=sqlhelper.select_excution("""
        select Bid from bill where Bstate = 1;
    """)
    shows={}
    for b in bills:
        rows=sqlhelper.select_excution("""
            select id,Dname,Sname,Dpice,nstate,B_D_T.Tid,Tname from B_D_T
            left join dish on B_D_T.Did=dish.Did
            left join Sort on dish.Soid=Sort.Soid
            left join Rtable on B_D_T.Tid=Rtable.Tid
            where Bid = %d
        """%b.Bid)
        psum=0
        for r in rows:
            if(r.nstate==3):
                psum+=r.Dpice
        shows[str(b.Bid)]={'disher':rows,'psum':psum}
    print(shows)
    return render_template('display_bill.html',shows=shows)

@app.route('/pay_bill/<Bid>')
def pay_bill(Bid):
    sqlhelper.insert_or_delet("""
        update bill set Bstate = 2 where Bid = %s
    """%Bid)
    sqlhelper.insert_or_delet("""
        update Rtable set Tstate = 0 where Tid in (select Tid from B_D_T where Bid = %s)
    """%Bid)
    return redirect(url_for('display_bill'))
