-- 1. 建立使用者表
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    city TEXT
);

-- 2. 建立訂單表
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_name TEXT,
    price REAL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- 3. 插入使用者資料
INSERT INTO users (user_id, user_name, city) VALUES
(1, 'Teddy', 'Kaohsiung'),
(2, 'Alice', 'Taipei'),
(3, 'Bob', 'Taichung'),
(4, 'Charlie', 'Tainan'); -- 這個人目前沒有訂單

-- 4. 插入訂單資料
INSERT INTO orders (order_id, user_id, product_name, price) VALUES
(101, 1, 'RTX 3060 12G', 8500.0),
(102, 1, 'Ryzen CPU', 6200.0),
(103, 2, 'Mechanical Keyboard', 2500.0),
(104, 3, '27-inch Monitor', 5500.0);