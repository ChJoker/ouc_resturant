# -*- coding: GBK -*-
from flask import request, redirect, url_for, send_from_directory, render_template, session, escape
from __init__ import app
from sqlHelper import sqlhelper

dishstate=app.config['DISH_STATE']

@app.route('/cookerlogin', methods=['GET', 'POST'])
def cookLogin():
    if request.method == 'GET':
        return render_template('cookerlogin.html')
    Rresult = sqlhelper.select_excution('''
        select Cnum,Sname,Cook.Soid,Cid from Cook,Sort where Cnum = %s and Cook.Soid=Sort.Soid;
    ''' % request.form['Cnum'])
    if (len(Rresult) != 1):
        return """
        <script>
             alert('not exist cooker number');
            history.go(-1);
         </script>
         """
    if not session.has_key('cooker'):
        cooker = {'Cnum':Rresult[0].Cnum,'Cid':Rresult[0].Cid,'Sname':Rresult[0].Sname,'Soid':Rresult[0].Soid}
        session.pop('cooker', None)
        session['cooker'] = cooker
    else:
        cooker = {'Cnum':Rresult[0].Cnum,'Cid':Rresult[0].Cid,'Sname':Rresult[0].Sname,'Soid':Rresult[0].Soid}
        session.pop('cooker', None)
        session['cooker'] = cooker
    return redirect(url_for('cook_job'))

@app.route('/cook_job')
def cook_job():
    unfinish=sqlhelper.select_excution("""
        select top 1 id,Dname,Dpic,Sname from B_D_T
            left join dish on B_D_T.Did=dish.Did
            left join Sort on dish.Soid=Sort.Soid
            where B_D_T.nstate = 1 and B_D_T.Cid = %s
            order by id
    """%session['cooker']['Cid'])
    if(len(unfinish)==1):
        return render_template('cook_job.html',row=unfinish[0])
    row=sqlhelper.select_excution("""
         select top 1 id,Dname,Dpic,Sname from B_D_T
            left join dish on B_D_T.Did=dish.Did
            left join Sort on dish.Soid=Sort.Soid
            where B_D_T.nstate = 0 and (dish.Soid = %s or Sort.Sname=N'家常菜')
            order by id
    """% str(session['cooker']['Soid']))
    if(len(row)>0):
        sqlhelper.insert_or_delet("""
            update B_D_T set nstate = 1,Cid=%s where id = %s
        """ % (session['cooker']['Cid'],row[0].id))
        return render_template('cook_job.html',row=row[0])
    return (render_template('cook_job.html'))


@app.route('/done_dish/<id>')
def done_dish(id):
    sqlhelper.insert_or_delet("""
            update B_D_T set nstate = 2 where id = %s
        """ % str(id))
    return redirect(url_for('cook_job'));

@app.route('/cancel_dish/<id>')
def cancel_dish(id):
    sqlhelper.insert_or_delet("""
            update B_D_T set nstate = 4 where id = %s
        """ % str(id))
    return redirect(url_for('cook_job'));




