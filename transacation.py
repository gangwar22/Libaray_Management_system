from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
from threading import Thread

transactions_bp = Blueprint('transactions', _name_)
mysql = MySQL()

@transactions_bp.route('/api/transactions', methods=['GET'])
def get_transactions():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    cursor.close()
    return jsonify(transactions)

# Add other CRUD operations for transactions (POST, PUT, DELETE)