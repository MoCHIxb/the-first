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
        return render_template('main.html',msg='登陆成功')############
    else:
        return render_template('login.html', msg='登录失败')#############
"""
@app.route('/register',methods=['GET','POST'])
def register():
    
"""

@app.route('/list',methods=['GET','POST'])
def list():
    sql = "select * from users"
    data=query(sql)
    db1,cursor1=get_db()
    if request.method == "POST":
        Name=request.form.get('Name',None)
        Points = request.form.get('Points',None)
        sql = "select id from users where username= '" + str(Name) + "'"
        res=query(sql)
        if res:
            insert = request.values.get("插入")
            sort_button = request.values.get("排序")
            print(Name,Points)
            if insert=='insert':
                if Name and Points:
                    insert_sql = "update users set point=" +str(Point+res[0][6])+" where username= '"+str(Name)+"'"##########
                    cursor1.execute(insert_sql)
                    db1.commit()
            if sort_button=='sort':
                sort_sql = "select * from users order by points desc limit 10"
                cursor1.execute(sort_sql)
                data = cursor1.fetchall()
        else:
            data='不是注册用户！'

    print(data)

    return render_template("list.html",data=data)



if __name__== '__main__':
    app.run()
