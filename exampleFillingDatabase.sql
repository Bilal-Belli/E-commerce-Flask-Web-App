-- Insert users
INSERT INTO users (username, password_hash, solde) VALUES
('alice', 'hashed_pw_alice', 100.50),
('bob', 'hashed_pw_bob', 200.00),
('charlie', 'hashed_pw_charlie', 50.75);

-- Insert products
INSERT INTO products (name, quantity, price) VALUES
('Laptop', 10, 1200.00),
('Headphones', 50, 150.00),
('Smartphone', 20, 800.00),
('Keyboard', 30, 50.00);

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