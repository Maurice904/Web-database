from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def check_validation(user, pwd):
    conn = pymysql.connect(host = "127.0.0.1", port = 3306, user = 'Tianhao', passwd = 'root123', charset = 'utf8', db = 'unicom')
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    sql = "select * from admin where username = %s"
    cursor.execute(sql, [user])
    pwd_lst = cursor.fetchall()
    cursor.close()
    conn.close()
    for dict_ in pwd_lst:
        if dict_['pwd'] == pwd:
            return True, True

    return False, False


@app.route('/register', methods = ['POST', 'GET'])
def do_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        print (user, pwd)
        return 'register complete'
    

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get('name_username')
        pwd = request.form.get('name_pwd')
        print (user, pwd)

        success, error = check_validation(user, pwd)
        if success:
            return redirect(url_for('success'))
        else:
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



if __name__ == '__main__':
    app.run()