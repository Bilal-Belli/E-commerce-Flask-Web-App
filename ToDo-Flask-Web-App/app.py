from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key
bcrypt = Bcrypt(app)

# MySQL configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "ecommerce"
}

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        solde = request.form['solde']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Insert new user into the database
            query = "INSERT INTO users (username, password_hash, solde) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, hashed_password, solde))
            connection.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            flash('Username already exists.', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Fetch user data from the database
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and bcrypt.check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/like', methods=['POST'])
def like_product():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to like products.'}), 401

    user_id = session['user_id']
    product_id = request.form.get('product_id')

    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required.'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Add product to favorites
        like_query = "INSERT IGNORE INTO likes (user_id, product_id) VALUES (%s, %s)"
        cursor.execute(like_query, (user_id, product_id))
        connection.commit()

        # Check if the product was actually inserted (not already liked)
        if cursor.rowcount > 0:
            message = "Product added to your favorites!"
        else:
            message = "Product was already in your favorites."

        return jsonify({'success': True, 'message': message})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch products with quantity > 0
        query = "SELECT * FROM products WHERE quantity > 0"
        cursor.execute(query)
        products = cursor.fetchall()

        # Handle 'add to basket' action
        if request.method == 'POST':
            product_id = request.form['product_id']
            action = request.form['action']

            if action == 'add_to_basket':
                # Add product to basket
                basket_query = """
                    INSERT INTO baskets (user_id, product_id, quantity)
                    VALUES (%s, %s, 1)
                    ON DUPLICATE KEY UPDATE quantity = quantity + 1
                """
                cursor.execute(basket_query, (user_id, product_id))
                connection.commit()
                flash("Product added to your basket!", "success")

        # Refresh the products list after any changes
        cursor.execute(query)
        products = cursor.fetchall()

    finally:
        cursor.close()
        connection.close()

    return render_template('home.html', products=products)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch favorite products
        query = """
            SELECT products.id AS product_id, products.name, products.quantity, products.price 
            FROM likes
            JOIN products ON likes.product_id = products.id
            WHERE likes.user_id = %s
        """
        cursor.execute(query, (user_id,))
        favorites = cursor.fetchall()

        if request.method == 'POST':
            action = request.form['action']
            product_id = request.form.get('product_id')

            if action == "remove":
                # Remove the selected product from favorites
                cursor.execute("DELETE FROM likes WHERE user_id = %s AND product_id = %s", (user_id, product_id))
                connection.commit()
                flash("Product removed from favorites.", "success")
    finally:
        cursor.close()
        connection.close()

    return render_template('favorites.html', favorites=favorites)

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch basket items
        query = """
            SELECT baskets.product_id, products.name, baskets.quantity, products.price, products.quantity AS stock_quantity 
            FROM baskets
            JOIN products ON baskets.product_id = products.id
            WHERE baskets.user_id = %s
        """
        cursor.execute(query, (user_id,))
        basket_items = cursor.fetchall()

        # Calculate total cost and fetch user's solde
        basket_total = sum(item['quantity'] * item['price'] for item in basket_items)
        cursor.execute("SELECT solde FROM users WHERE id = %s", (user_id,))
        user_solde = cursor.fetchone()['solde']

        if request.method == 'POST':
            action = request.form['action']
            product_id = request.form.get('product_id')

            if action == "remove":
                # Remove the selected product from the basket
                cursor.execute("DELETE FROM baskets WHERE user_id = %s AND product_id = %s", (user_id, product_id))
                connection.commit()
                flash("Product removed from basket.", "success")

            elif action == "purchase":
                if basket_total > user_solde:
                    flash("Insufficient solde to complete the purchase.", "danger")
                else:
                    # Deduct user's solde and update product quantities
                    cursor.execute("UPDATE users SET solde = solde - %s WHERE id = %s", (basket_total, user_id))
                    for item in basket_items:
                        new_quantity = item['stock_quantity'] - item['quantity']
                        cursor.execute(
                            "UPDATE products SET quantity = %s WHERE id = %s", 
                            (new_quantity, item['product_id'])
                        )
                    # Clear the user's basket
                    cursor.execute("DELETE FROM baskets WHERE user_id = %s", (user_id,))
                    connection.commit()
                    flash("Purchase completed successfully!", "success")
                    return redirect(url_for('home'))

        # Refresh basket items and total cost after any changes
        cursor.execute(query, (user_id,))
        basket_items = cursor.fetchall()
        basket_total = sum(item['quantity'] * item['price'] for item in basket_items)

    finally:
        cursor.close()
        connection.close()

    return render_template('basket.html', basket_items=basket_items, basket_total=basket_total, user_solde=user_solde)

if __name__ == '__main__':
    app.run(debug=True)