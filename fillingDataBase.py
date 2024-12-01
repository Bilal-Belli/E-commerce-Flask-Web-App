import mysql.connector
from mysql.connector import Error
import random
import string

# Function to generate random product names
def random_product_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to populate the database with a lot of products
def populate_products(connection, num_products):
    cursor = connection.cursor()
    products = [
        (random_product_name(), random.randint(1, 1000), round(random.uniform(1.0, 1000.0), 2))
        for _ in range(num_products)
    ]
    query = "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)"
    cursor.executemany(query, products)
    connection.commit()
    print(f"{num_products} products inserted successfully.")

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
        
        # Populate products table with 1000 random products
        populate_products(connection, 1000)

except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        connection.close()
        print("Database connection closed")