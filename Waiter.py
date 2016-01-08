# -*- coding: GBK -*-
from flask import request, redirect, url_for, send_from_directory, render_template, session, escape
from __init__ import app
from sqlHelper import sqlhelper

dishstate=app.config['DISH_STATE']
@app.route('/waiterLogin', methods=['GET', 'POST'])
def waiterLogin():
    if request.method == 'GET':
        return render_template('waiterLogin.html')
    Rresult = sqlhelper.select_excution('''
        select * from Rtable where Tid = %s;
    ''' % request.form['Tid'])
    Wresult = sqlhelper.select_excution('''
        select * from Waiter where Wnum = '%s';
    ''' % request.form['Wnum'])
    if (len(Rresult) != 1 or len(Wresult) != 1):
         return """
            <script>
             alert('不存在桌号或工号');
             history.go(-1);
            </script>
         """
    print(Rresult)
    if(Rresult[0].Tstate == 0):
         return """
            <script>
             alert('桌子没有客人');
             history.go(-1);
            </script>
         """
    if not session.has_key('menu'):
        menu = {'Tid':request.form['Tid'],'Wnum':request.form['Wnum'],'sum':0,'dishes':[],'Psum':0,'state':0}
        session.pop('menu', None)
        session['menu'] = menu
    return redirect(url_for('all_dishes'))

@app.route('/all_dishes')
@app.route('/all_dishes/<Soid>/<int:page>')
def all_dishes(Soid = '-1',page=1):
    print(session['menu'])
    if session['menu']['state'] !=0:
        return redirect(url_for('wait_dishes'))
    if(Soid=='-1'):
        Asum=int(sqlhelper.select_excution("""
            select count(*) from dish
        """)[0][0])
    else:
        Asum = int(sqlhelper.select_excution("""
            select count(*) from dish where Soid = %s
        """ % Soid)[0][0])
    print(Asum)
    if(page<1):
        page=1
    if(page>(Asum-1)/6+1):
        page=(Asum-1)/6+1
    sorts = sqlhelper.select_excution("""
        select Soid,Sname from Sort;
    """)
    if(Soid=='-1'):
        dishes = sqlhelper.select_excution("""
            select top 6 Did,Dname,Dpice,Dpic from dish where Did not in (select top %d Did from dish);
        """ % ((page-1)*6))
    else:
        dishes = sqlhelper.select_excution("""
            select top 6 Did,Dname,Dpice,Dpic from dish where Soid = %s and Did not in (select top %d Did from dish where Soid = %s);
        """ % (Soid,(page-1)*6,Soid))
    return render_template('order_dish.html',page=page,dishes=dishes,sorts=sorts,Soid=int(Soid))

@app.route('/order_dish/<Did>/<Dname>/<Dprice>')
def order_dish(Did , Dname , Dprice):
    old_menu=session['menu']
    print(old_menu)
    old_menu['sum']+=1
    old_menu['dishes'].append({'Did':Did,'Dname':Dname,'Dprice':Dprice})
    old_menu['Psum']+=float(Dprice)
    return '1'

@app.route('/del_dish/<Did>')
def del_dish(Did):
    if session['menu']['state'] !=0:
        return redirect(url_for('wait_dishes'))
    old_menu = session['menu']
    print(old_menu)
    for i in range(len(old_menu['dishes'])):
        if(old_menu['dishes'][i]['Did'] == Did):
            old_menu['Psum']-=float(old_menu['dishes'][i]['Dprice'])
            old_menu['sum']-=1
            del old_menu['dishes'][i]
            return render_template('sure_order.html')
    return render_template('sure_order.html')

@app.route('/sure_order')
def sure_order():
    if session['menu']['state'] !=0:
        return redirect(url_for('wait_dishes'))
    return render_template('sure_order.html')

@app.route('/order_order')
def order_order():
    Bid = sqlhelper.insert_get_seed("""
        insert into bill (Bsun,Bstate) values (%f,0)
    """ %  session['menu']['Psum'])
    for d in session['menu']['dishes']:
        sqlhelper.insert_or_delet("""
            insert into B_D_T (Bid,Did,Tid,nstate) values (%s,%s,%s,0)
        """% (str(Bid),str(d['Did']),str(session['menu']['Tid'])))
    session['menu']['state']=1
    session['menu']['Bid']=str(Bid)
    print(session['menu'])
    return render_template('wait_dishes.html',dishes=sqlhelper.select_excution("""
        select id,Dname,Dpice,nstate from B_D_T left join dish on B_D_T.Did = dish.Did where B_D_T.Bid = %s
    """% str(Bid)))

@app.route('/wait_dishes')
def wait_dishes():
    return render_template('wait_dishes.html',dishes=sqlhelper.select_excution("""
        select id,Dname,Dpice,nstate from B_D_T left join dish on B_D_T.Did = dish.Did where B_D_T.Bid = %s
    """% str(session['menu']['Bid'])))

@app.route('/send_dish/<id>')
def send_dish(id):
    sqlhelper.insert_or_delet("""
        update B_D_T set nstate=3 where id = %s
    """% str(id))
    return redirect(url_for('wait_dishes'))

@app.route('/cancal_order')
def cancal_order():
    sqlhelper.insert_get_seed("""
       update B_D_T set nstate=%s where Bid = %s and nstate=0;
    """ % (str(dishstate['cancel']),str(session['menu']['Bid'])))
    return redirect(url_for('wait_dishes'))

@app.route('/finish_order')
def finish_order():
    rows = sqlhelper.select_excution("""
        select * from B_D_T where nstate != 3 and nstate !=4 and Bid = %s
    """ % str(session['menu']['Bid']))
    if len(rows) != 0 :
        return """
        <script>
            alert("you can't do that,still unfinish dish");
            history.go(-1);
        </script>
        """
    sqlhelper.insert_or_delet("""
        update bill set Bstate = 1 where Bid = %s
    """% str(session['menu']['Bid']))
    session.pop('menu', None)
    return redirect(url_for('waiterLogin'))



