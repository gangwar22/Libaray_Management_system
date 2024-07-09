from flask import Blueprint, jsonify, request, make_response, current_app
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

users_bp = Blueprint('users', _name_)
mysql = MySQL()

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    hashed_password = generate_password_hash(password, method='sha256')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data['username']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[2], password):
        token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@users_bp.route('/', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()

    return jsonify(users)

# Add other CRUD operations for users (GET by id, PUT, DELETE)