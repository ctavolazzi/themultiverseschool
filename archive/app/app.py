from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib
import webbrowser
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_user():
    if not os.path.exists('user_profile.json'):
        return None
    with open('user_profile.json') as f:
        return json.load(f)

@app.route('/')
def home():
    if 'username' in session:
        user = load_user()
        if user:
            return render_template('dashboard.html', user=user)
        else:
            return redirect(url_for('create_profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = load_user()
    if not user:
        return redirect(url_for('create_profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username == user['username'] and hashed_password == user['password_hash']:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_profile = {
            "username": username,
            "password_hash": hashed_password,
            "created_at": datetime.datetime.now().isoformat()
        }
        with open('user_profile.json', 'w') as f:
            json.dump(user_profile, f, indent=4)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('create_profile.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run()
