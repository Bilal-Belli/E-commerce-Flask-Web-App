-- Insert users
INSERT INTO users (username, password_hash, solde) VALUES
('alice', 'hashed_pw_alice', 100.50),
('bob', 'hashed_pw_bob', 200.00),
('charlie', 'hashed_pw_charlie', 50.75);

-- Insert categories
INSERT INTO categories (name) VALUES
('Electronics'),
('Accessories'),
('Mobile Devices'),
('Peripherals');

-- Insert products (with category and image path)
INSERT INTO products (name, category_id, quantity, price, image_path) VALUES
('Laptop', 1, 10, 1200.00, 'http://res.cloudinary.com/dxqcqtzo2/image/upload/v1733321517/gabmhjob2hlts1hxmuhs.jpg'),
('Headphones', 2, 50, 150.00, 'http://res.cloudinary.com/dxqcqtzo2/image/upload/v1733321518/ybbxmtibkmxezjwjfhbh.jpg'),
('Smartphone', 3, 20, 800.00, 'http://res.cloudinary.com/dxqcqtzo2/image/upload/v1733321519/heunqjkzwauzxaoisufb.jpg'),
('Keyboard', 4, 30, 50.00, 'http://res.cloudinary.com/dxqcqtzo2/image/upload/v1733321520/lg4qenrw5az0hj9pcr4y.jpg');

-- Insert basket items
INSERT INTO baskets (user_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(3, 4, 1);

-- Insert likes
INSERT INTO likes (user_id, product_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4);