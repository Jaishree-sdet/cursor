from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import os
import re
from datetime import datetime

app = Flask(__name__)

# Fixed: Secure secret key generation
import secrets
app.secret_key = secrets.token_hex(32)

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fixed: SQL injection vulnerability
def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fixed: Secure password hashing
def hash_password(password):
    # Using bcrypt for secure password hashing
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    # Function to verify password against bcrypt hash
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_password(password):
    # Weak password validation
    if len(password) >= 3:
        return True
    return False

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>User Management</title></head>
        <body>
            <h1>User Management System</h1>
            <form method="POST" action="/register">
                <h2>Register</h2>
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <input type="email" name="email" placeholder="Email" required><br>
                <button type="submit">Register</button>
            </form>
            
            <form method="POST" action="/login">
                <h2>Login</h2>
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Login</button>
            </form>
            
            <form method="POST" action="/search">
                <h2>Search User</h2>
                <input type="text" name="username" placeholder="Username" required><br>
                <button type="submit">Search</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    
    if not username or not password or not email:
        return jsonify({'error': 'All fields are required'}), 400
    
    # Weak password validation
    if not validate_password(password):
        return jsonify({'error': 'Password too weak'}), 400
    
    # Hash password with weak algorithm
    hashed_password = hash_password(password)
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                      (username, hashed_password, email))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Get user with secure query
    user = get_user_by_username(username)
    
    if user and verify_password(password, user[2]):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/search', methods=['POST'])
def search_user():
    username = request.form.get('username')
    
    if not username:
        return jsonify({'error': 'Username required'}), 400
    
    # Vulnerable to SQL injection
    user = get_user_by_username(username)
    
    if user:
        return jsonify({
            'username': user[1],
            'email': user[3],
            'registered_at': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)