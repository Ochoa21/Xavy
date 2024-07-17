from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        otp_secret TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    password = data['password']
    otp_secret = data['otp_secret']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, otp_secret) VALUES (?, ?, ?)", (username, password, otp_secret))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password, otp_secret FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        return jsonify({"otp_secret": result[1]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000)
