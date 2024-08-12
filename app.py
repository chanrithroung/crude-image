from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL 
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'FlaskDB'
mysql = MySQL(app)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    connection = mysql.connection.cursor()
    connection.execute("SELECT * FROM tbProduct ")
    data = connection.fetchall()
    connection.close()
    return render_template('index.html', products=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        img = request.files['image']
        if img:
            img_filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        else:
            img_filename = None
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO tbProduct(name, description, image) VALUES ('{name}','{description}', '{img_filename}')")
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `tbProduct` WHERE `id` = '{id}' ")
    data = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
       
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        else: 
            image_filename = data[4]
        cur.execute(f"UPDATE `tbProduct` SET `name`='{name}',`description`='{description}',`image`='{image_filename}' WHERE `id` = '{id}'")
        mysql.connection.commit()
        return redirect(url_for('index'))
        
    return render_template('edit.html', product=data)

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM tbProduct WHERE id = {id}")
    mysql.connection.commit()
    return redirect(url_for('index'))
    
    

if __name__ == '__main__':
    app.run()