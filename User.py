from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rahul@123'
app.config['MYSQL_DB'] = 'rahul_'

mysql = MySQL(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = generate_password_hash(data['password'])
    name = data['name']
    phone_number = data.get('phone_number', '')

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO users (email, password, name, phone_number) VALUES (%s, %s, %s, %s)', 
                   (email, password, name, phone_number))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Signup successful!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[2], password):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Login failed!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
