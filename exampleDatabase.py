import mysql.connector
from mysql.connector import Error

# Sample data
users = [
    {"username": "alice", "password_hash": "hashed_pw_alice", "solde": 100.50},
    {"username": "bob", "password_hash": "hashed_pw_bob", "solde": 200.00},
    {"username": "charlie", "password_hash": "hashed_pw_charlie", "solde": 50.75},
]

products = [
    {"name": "Laptop", "quantity": 10, "price": 1200.00},
    {"name": "Headphones", "quantity": 50, "price": 150.00},
    {"name": "Smartphone", "quantity": 20, "price": 800.00},
    {"name": "Keyboard", "quantity": 30, "price": 50.00},
]

basket_items = [
    {"user_id": 1, "product_id": 1, "quantity": 1},
    {"user_id": 1, "product_id": 2, "quantity": 2},
    {"user_id": 2, "product_id": 3, "quantity": 1},
    {"user_id": 3, "product_id": 4, "quantity": 1},
]

likes = [
    {"user_id": 1, "product_id": 1},
    {"user_id": 1, "product_id": 2},
    {"user_id": 2, "product_id": 3},
    {"user_id": 3, "product_id": 4},
]

# Function to insert data into a table
def insert_data(connection, table, data):
    cursor = connection.cursor()
    for row in data:
        columns = ", ".join(row.keys())
        placeholders = ", ".join(["%s"] * len(row))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(row.values()))
    connection.commit()

try:
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="ecommerce"
    )
    
    if connection.is_connected():
        print("Connected to the database")

        # Populate tables
        insert_data(connection, "users", users)
        insert_data(connection, "products", products)
        insert_data(connection, "baskets", basket_items)
        insert_data(connection, "likes", likes)

        print("Database populated successfully")

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        connection.close()
        print("Database connection closed")