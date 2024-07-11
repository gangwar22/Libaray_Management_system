# from flask import Blueprint, jsonify, request
# from flask_mysqldb import MySQL
# from threading import Thread

# borrowers_bp = Blueprint('borrowers', __name__)
# mysql = MySQL()

# @borrowers_bp.route('/api/borrowers', methods=['GET'])
# def get_borrowers():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM borrowers")
#     borrowers = cursor.fetchall()
#     cursor.close()
#     return jsonify(borrowers)

# # Add other CRUD operations for borrowers (POST, PUT, DELETE)
