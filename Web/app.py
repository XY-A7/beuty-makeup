import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 用户数据文件
USER_DATA_FILE = "userdata.csv"

# 检查用户是否存在
def user_exists(username):
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row and row[0] == username:
                    return True
    except FileNotFoundError:
        pass
    return False

# 获取用户密码
def get_user_password(username):
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row and row[0] == username:
                    return row[1]
    except FileNotFoundError:
        pass
    return None

# 添加用户
def add_user(username, password):
    with open(USER_DATA_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([username, password])

# 检查文件是否存在，如果不存在则创建并写入标题行
def initialize_user_file():
    try:
        with open(USER_DATA_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            pass
    except FileNotFoundError:
        with open(USER_DATA_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['username', 'password'])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def index_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username")
    pwd = request.form.get("password")
    
    if user_exists(name):
        stored_password = get_user_password(name)
        if pwd == stored_password:
            return redirect(url_for('index'))  # 登录成功后重定向到首页
        else:
            return '密码错误 <a href="/login">返回登录界面</a>'
    else:
        return '用户不存在 <a href="/login">返回登录界面</a>'

@app.route("/register", methods=["GET"])
def index_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("username")
    pwd = request.form.get("password")
    
    if user_exists(name):
        return '用户已存在 <a href="/login">返回登录界面</a>'
    else:
        add_user(name, pwd)
        return redirect(url_for('index_login'))  # 注册成功后重定向到登录页面

@app.route("/shopping")
def shopping():
    return render_template("shopping.html")

if __name__ == "__main__":
    initialize_user_file()
    app.run(debug=True)