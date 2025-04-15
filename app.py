from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

USER_FILE = 'users.json'

# 사용자 파일이 없다면 초기화
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users:
            return "이미 존재하는 아이디입니다. <a href='/register'>다시 시도</a>"
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users and users[username] == password:
            return render_template('dashboard.html', username=username)
        return "로그인 실패! <a href='/login'>다시 시도</a>"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
