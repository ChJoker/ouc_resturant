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
    return redirect(url_for('dishes'))
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file',
                                    filename=file.filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data accept-charset=utf-8>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
    savefile = str(uuid.uuid1()) + '.' + file.filename.rsplit('.', 1)[1];
    if file and allowed_file(savefile):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], savefile))
    result = sqlhelper.insert_or_delet("""
        insert into dish (Soid,Dname,Dpice,Dpic) values (%s,N'%s',%f,'%s');
    """ % (request.form['Soid'], request.form['Dname'], float(request.form['Dpice']), savefile))
    return redirect(url_for('add_dish'))
