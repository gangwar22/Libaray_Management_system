from flask import Flask, request, jsonify
from flask_cors import CORS
import mariadb
import sys

app = Flask(__name__)
CORS(app)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root123",
        host="localhost",
        port=3306,
        database="PublicBookLibrary"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
print("Connected to MariaDB")

# Helper function to convert query results to dictionary
def dict_from_row(row):
        return {cur.description[i][0]: row[i] for i in range(len(row))}

def CreateTables(tablename):
    print("Creating table:", tablename)
    # Create the SQL command dynamically
    create_table_command = f"""
    CREATE TABLE IF NOT EXISTS {tablename} (
        book_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(100) NOT NULL,
        genre VARCHAR(50),
        isbn VARCHAR(20),
        publisher VARCHAR(100),
        publish_date DATE,
        quantity INT NOT NULL DEFAULT 0,
        available INT NOT NULL DEFAULT 0
    );
    """
    
    # Execute the SQL command
    cur.execute(create_table_command)
    conn.commit()

# Call the function to create the table
# CreateTables("books")

# CRUD operations for books

# Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    
    data = request.get_json()
    
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    isbn = data.get('isbn')
    publisher = data.get('publisher')
    publish_date = data.get('publish_date')
    quantity = data.get('quantity')
    available = data.get('available')
    
    try:
        cur.execute(
            "INSERT INTO books (title, author, genre, isbn, publisher, publish_date, quantity, available) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (title, author, genre, isbn, publisher, publish_date, quantity, available)
        )
        conn.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500
    
# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    try:
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        newdataarr = []
        for row in rows:
            data = dict_from_row(row)
            newdataarr.append(data)

        books = [dict_from_row(row) for row in rows]
        print(books)
        return jsonify(books), 200
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({"message": "Book deleted successfully"}), 200
        else:
            return jsonify({"message": "Book not found"}), 404
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500


# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    isbn = data.get('isbn')
    publisher = data.get('publisher')
    publish_date = data.get('publish_date')
    quantity = data.get('quantity')
    available = data.get('available')
    
    try:
        cur.execute(
            "UPDATE books SET title = ?, author = ?, genre = ?, isbn = ?, publisher = ?, publish_date = ?, quantity = ?, available = ? WHERE book_id = ?",
            (title, author, genre, isbn, publisher, publish_date, quantity, available, book_id)
        )
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({"message": "Book updated successfully"}), 200
        else:
            return jsonify({"message": "Book not found"}), 404
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500

# Read a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        row = cur.fetchone()
        if row:
            book = dict_from_row(row)
            return jsonify(book), 200
        else:
            return jsonify({"message": "Book not found"}), 404
    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500








if __name__ == '__main__':
    app.run(debug=True)
