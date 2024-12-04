-- Insert users
INSERT INTO users (username, password_hash, solde) VALUES
('alice', 'hashed_pw_alice', 100.50),
('bob', 'hashed_pw_bob', 200.00),
('charlie', 'hashed_pw_charlie', 50.75);

-- -- Insert products
-- INSERT INTO products (name, quantity, price) VALUES
-- ('Laptop', 10, 1200.00),
-- ('Headphones', 50, 150.00),
-- ('Smartphone', 20, 800.00),
-- ('Keyboard', 30, 50.00);

-- -- Insert basket items
-- INSERT INTO baskets (user_id, product_id, quantity) VALUES
-- (1, 1, 1),
-- (1, 2, 2),
-- (2, 3, 1),
-- (3, 4, 1);

-- -- Insert likes
-- INSERT INTO likes (user_id, product_id) VALUES
-- (1, 1),
-- (1, 2),
-- (2, 3),
-- (3, 4);


INSERT INTO categories (name) VALUES
('Electronics'),
('Accessories'),
('Books'),
('Clothing'),
('Home Appliances');


-- Note: Replace '/path/to/image.jpg' with the actual image path on your server or system.

INSERT INTO products (name, quantity, price, image, category_id) VALUES
('Laptop', 10, 1200.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\laptop.jpg'), 1),
('Headphones', 50, 150.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\headphones.jpg'), 2),
('Smartphone', 20, 800.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\smartphone.jpg'), 1),
('Keyboard', 30, 50.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\keyboard.jpg'), 2),
('Fiction Book', 100, 20.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\book.jpg'), 3),
('Winter Jacket', 15, 120.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\jacket.jpg'), 4),
('Microwave Oven', 5, 250.00, LOAD_FILE('C:\Users\Hp\OneDrive\Bureau\flaskUpworkGit\imagesExamples\microwave.jpg'), 5);


-- User Alice (id=1) buys a Laptop and a Winter Jacket.
-- User Bob (id=2) buys a Smartphone.
-- User Charlie (id=3) buys a Fiction Book and Headphones.

INSERT INTO baskets (user_id, product_id, quantity) VALUES
(1, 1, 1),  -- Alice buys 1 Laptop
(1, 6, 1),  -- Alice buys 1 Winter Jacket
(2, 3, 1),  -- Bob buys 1 Smartphone
(3, 5, 2),  -- Charlie buys 2 Fiction Books
(3, 2, 1);  -- Charlie buys 1 Headphones


-- Users like various products.

INSERT INTO likes (user_id, product_id) VALUES
(1, 1),  -- Alice likes Laptop
(1, 6),  -- Alice likes Winter Jacket
(2, 3),  -- Bob likes Smartphone
(3, 5),  -- Charlie likes Fiction Book
(3, 2);  -- Charlie likes Headphones