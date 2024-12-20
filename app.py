from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template_string
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

# "host" for deployement : raedaltomy.mysql.pythonanywhere-services.com
# "user": raedaltomy
# "password": "1A2Z3E4R"
# "database": "raedaltomy$ecommerce"

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        solde = request.form['solde']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Check if username already exists
            check_query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(check_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists. Please choose a different one.', 'danger')
            else:
                # Insert new user into the database
                query = "INSERT INTO users (username, password_hash, solde) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, hashed_password, solde))
                connection.commit()
                flash('Account created successfully. Please log in.', 'success')
                return redirect(url_for('login'))
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
        # Fetch products with their category names and quantity > 0
        query = """
            SELECT products.*, categories.name AS category_name 
            FROM products 
            LEFT JOIN categories ON products.category_id = categories.id 
            WHERE products.quantity > 0
        """
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
        if request.method == 'POST':
            action = request.form.get('action')
            product_id = request.form.get('product_id')

            if action == "remove":
                # Remove the selected product from favorites
                cursor.execute("DELETE FROM likes WHERE user_id = %s AND product_id = %s", (user_id, product_id))
                connection.commit()
                return jsonify({"success": True, "message": "Product removed successfully"})

        # Fetch favorite products for initial page load
        query = """
            SELECT products.id AS product_id, products.name, products.quantity, products.price 
            FROM likes
            JOIN products ON likes.product_id = products.id
            WHERE likes.user_id = %s
        """
        cursor.execute(query, (user_id,))
        favorites = cursor.fetchall()
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

@app.route('/filter_products')
def filter_products():
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', float('inf')))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
            SELECT products.*, categories.name AS category_name 
            FROM products 
            LEFT JOIN categories ON products.category_id = categories.id 
            WHERE products.price BETWEEN %s AND %s AND products.quantity > 0
        """
        cursor.execute(query, (min_price, max_price))
        filtered_products = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template_string('''
        {% for product in products %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="{{ product.image_path }}" class="card-img-top" alt="{{ product.name }}" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <span class="badge bg-secondary">{{ product.category_name }}</span>
                        <p class="card-text">
                            <strong>Price:</strong> ${{ product.price }}<br>
                            <strong>Quantity:</strong> {{ product.quantity }}
                        </p>
                        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#productModal{{ product.id }}">
                            View Details
                        </button>
                        <form method="post" class="d-flex justify-content-between mt-2">
                            <input type="hidden" name="product_id" value="{{ product.id }}">
                            <button type="button" class="btn btn-outline-primary like-btn" data-product-id="{{ product.id }}">
                                <i class="fas fa-heart"></i> Like
                            </button>
                            <button type="submit" name="action" value="add_to_basket" class="btn btn-outline-success">
                                <i class="fas fa-shopping-cart"></i> Add to Basket
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Modal for Product Details -->
                <div class="modal fade" id="productModal{{ product.id }}" tabindex="-1" aria-labelledby="productModalLabel{{ product.id }}" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="productModalLabel{{ product.id }}">{{ product.name }}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <img src="{{ product.image_path }}" alt="{{ product.name }}" class="img-fluid mb-3">
                                <p><strong>Category:</strong> {{ product.category_name }}</p>
                                <p><strong>Price:</strong> ${{ product.price }}</p>
                                <p><strong>Quantity:</strong> {{ product.quantity }}</p>
                                <!-- Add more detailed information here if needed -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    ''', products=filtered_products)

if __name__ == '__main__':
    app.run(debug=True)