from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import pymysql
import os

app = Flask(__name__)
app.secret_key =os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

def load_user(user_id):
    conn = pymysql.connect(host=os.getenv("DB_HOST", "127.0.0.1"), 
                           user=os.getenv("DB_USER", "Tianhao"), 
                           passwd=os.getenv("DB_PASSWORD", "root123"), 
                           db=os.getenv("DB_NAME", "unicom"), 
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM admin WHERE id = %s", (user_id,))
    user_record = cursor.fetchone()
    if user_record:
        user = User()
        user.id = user_record['id']
        return user
    return None

def check_validation(username, password):
    conn = pymysql.connect(host=os.getenv("DB_HOST", "127.0.0.1"), 
                           user=os.getenv("DB_USER", "Tianhao"), 
                           passwd=os.getenv("DB_PASSWORD", "root123"), 
                           db=os.getenv("DB_NAME", "unicom"), 
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
    user_record = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_record and bcrypt.check_password_hash(user_record['pwd'], password):
        return user_record['id']
    return None

@app.route('/register', methods = ['POST', 'GET'])
def do_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        print (user, pwd)
        return 'register complete'
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('manage'))

    if request.method == 'POST':
        username = request.form['name_username']
        password = request.form['name_pwd']
        user_id = check_validation(username, password)
        if user_id:
            user = User()
            user.id = user_id
            login_user(user)
            return redirect(url_for('success'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


@app.route('/create', methods = ['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        user = request.form.get('name_username')
        pwd = request.form.get('name_pwd')
        first_name = request.form.get('name_first')
        last_name = request.form.get('name_last')
        age = request.form.get('name_age')
        mobile = request.form.get("name_mobile")
        if user and pwd and age and mobile and first_name and last_name:
            
            conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
            cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
            sql = "insert into admin (username, pwd, first_name, last_name, age, mobile) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, [user,pwd,first_name,last_name,age,mobile])
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('created'))

        else:
            return render_template('create.html')


@app.route('/manage')
@login_required
def manage():
    conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    sql = "select * from admin"
    cursor.execute(sql)
    dict_lst = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('account_manage.html', dict_lst = dict_lst)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/created')
def created():
    return render_template('account_created.html')

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    sql = "delete from admin where id = %s"
    cursor.execute(sql, item_id)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('manage'))

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if request.method == 'POST':
        user = request.form.get('name_username')
        pwd = request.form.get('name_pwd')
        first_name = request.form.get('name_first')
        last_name = request.form.get('name_last')
        age = request.form.get('name_age')
        mobile = request.form.get("name_mobile")
        if user and pwd and age and mobile and first_name and last_name:
            
            conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
            cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
            sql = "update admin set username = %s, pwd = %s, first_name = %s, last_name = %s, age = %s, mobile = %s where id = %s"
            cursor.execute(sql, [user, pwd, first_name, last_name, age, mobile, user_id])
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('manage'))
        
        return redirect(url_for('manage'))
    else:
        conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
        cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
        sql = "SELECT * FROM admin WHERE id = %s"
        cursor.execute(sql, user_id)
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit.html', user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()