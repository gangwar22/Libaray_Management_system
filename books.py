# from flask import Blueprint, jsonify, request
# from flask_mysqldb import MySQL
# from threading import Thread

# books_bp = Blueprint('books', __name__)
# mysql = MySQL()

# @books_bp.route('/api/books', methods=['GET'])
# def get_books():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM books")
#     books = cursor.fetchall()
#     cursor.close()
#     return jsonify(books)

# # Add other CRUD operations for books (POST, PUT, DELETE)
