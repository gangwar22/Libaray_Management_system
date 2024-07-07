import mysql.connector

# Connect to MariaDB
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Rahul@123',  # Replace with your MariaDB root password
        database='rahul_',  # Replace with your database name
        charset="utf8mb4",
        collation="utf8mb4_general_ci"
    )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print(f"Connected to MariaDB Server version {db_Info}")
        
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to create a table
        create_table_query = """
            CREATE TABLE user_information (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL
            )
        """

        # Execute the CREATE TABLE query
        cursor.execute(create_table_query)
        print("Table 'user_info' created successfully.")

        # Commit changes to the database
        connection.commit()

except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

finally:
    # Close database connection and cursor
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MariaDB connection is closed")