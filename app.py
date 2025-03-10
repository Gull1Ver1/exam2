import os
import sqlite3
import webbrowser
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session
)


UPLOAD_FOLDER = 'static/img'

from models.users import start_db


app = Flask(__name__)
app.secret_key = 'Era228'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

start_db()


@app.route('/', methods=['GET', 'POST'])
def get_base():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall() 

    conn.close()
    return render_template('base.html', posts=posts)



@app.route('/profile', methods=['GET','POST'])
def get_profile():
    login = session.get('login', 'Гость')
    return render_template('profile.html')



@app.route('/uslugi', methods=['GET','POST'])
def get_uslugi():
    return render_template('uslugi.html')


@app.route('/create_post', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        file = request.files['photo']

        if file:
            #  имя файла напрямую
            filename = file.filename
            
            #  изображение в папку static/img
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            conn = sqlite3.connect('post.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO post (title, description, price, photo_path)
                VALUES (?, ?, ?, ?)
            """, (title, description, price, file_path))
            conn.commit()
            conn.close()

            return redirect(url_for('get_base'))

    return render_template('create.html')





@app.route('/reg', methods=['GET','POST'])
def get_reg():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)
        session['login'] = request.form.get('login')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (login, email, password) VALUES (?, ?, ?)', (login, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('get_base'))

    return render_template('reg.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('login',None)
    return redirect(url_for('get_base'))


if __name__ == '__main__':
    app.run(debug=True)