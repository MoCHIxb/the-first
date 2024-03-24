from flask import Flask
from flask import request
from flask import render_template
import mysql.connector

app=Flask(__name__)

######################################
def get_db(): #打开mysql
    db=mysql.connector.connect(
        host='localhost',
        user='root',
        password='936855085chimo@',
        db="register",
        charset="utf8"
    )
    cursor=db.cursor()
    return db, cursor

def close_db(db, cursor):  # 关闭mysql
    if cursor:
        cursor.close()
    if db:
        db.close()
        
def query(sql, *args):  # 查询模块
    db, cursor = get_db()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    db.commit()
    close_db(db, cursor)
    return res

def get_user(username, password):  # 从数据库中查询用户名和密码
    sql = "select id from users where username= '" + str(username) + "' and password= '" + str(password) + "'"
    res = query(sql)
    return res


######################################
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    username = request.form.get('username')  # 接收form表单传参
    password = request.form.get('password')
    res = get_user(username, password)
    if res:
        return render_template('main.html',msg='登陆成功')
    else:
        return render_template('login.html', msg='登录失败')
"""
@app.route('/register',methods=['GET','POST'])
def register():
    
"""
if __name__== '__main__':
    app.run()
