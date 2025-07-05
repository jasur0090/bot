import sqlite3


def create_users_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            telegram_id BIGINT NOT NULL UNIQUE,
            phone TEXT
        );
        ''')
    database.commit()
    database.close()


# create_users_table()


def create_carts_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id),
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0
        );
        ''')
    database.commit()
    database.close()


# create_carts_table()


def create_cart_products_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(30),
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,
        cart_id INTEGER REFERENCES carts(cart_id),
        
        UNIQUE(product_name, cart_id)
        );
        ''')
    database.commit()
    database.close()


# create_cart_products_table()


def create_categories_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(30) NOT NULL UNIQUE
    );
    ''')
    database.commit()
    database.close()


# create_categories_table()


def insert_categories():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES 
    ('Lavash 🌯'),
    ('Burger 🍔'),
    ('Shaurma 🥙'),
    ('Hot-dog 🌭'),
    ('Disert 🍰'),
    ('Napitkalar 🥤')
    ''')
    database.commit()
    database.close()


# insert_categories()


def create_products_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(30) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        description TEXT,
        image TEXT,
        
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
        );
        ''')
    database.commit()
    database.close()


# create_products_table()


def insert_products_table():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image) VALUES
    (1, 'Fitter', 25000, 'Ichi to`la gazon va umuman toymisiz', 'media/lavash/fitter_lavash.jpg'),
    (1, 'Mol achchiq', 28000, 'Achchiq gosht va sochni bodringi bilan', 'media/lavash/mol_achchiq_lavash.jpg'),
    (1, 'Mol sir', 30000, 'Mol sirli parmizan db oylamen', 'media/lavash/mol_sirli_lavash.jpg'),
    (1, 'Tovuq achchiq', 28000, 'Achchiq tovuq goshtli va sochni', 'media/lavash/tovuq_achchiq_lavash.jpg'),
    (1, 'Tovuq sir', 29000, 'Tovuq goshtli sirli pamidor bonusiga', 'media/lavash/tovuq_sirli_lavash.jpg'),
    (1, 'Tovuq gosht', 27000, 'Tovuq goshtli sirsiz pamidor bonusiga', 'media/lavash/tovuqli_lavash.jpg')
    ''')
    database.commit()
    database.close()


# insert_products_table()


# Eski mijozlani bazadan qidiradi !
def first_select_user(chat_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


# Yangi mijozlani royxatdan otqazadi !
def first_register_user(chat_id, full_name):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES(?, ?)
    ''', (chat_id, full_name))
    database.commit()
    database.close()


# Tel raqamni olish
def update_user_to_finish_register(chat_id, phone):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
        UPDATE users
        SET phone = ?
        WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES
    (
    (SELECT user_id FROM users WHERE telegram_id = ?)
    )
    ''', (chat_id,))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category_id(category_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name
    FROM products WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products


def get_product_detail(product_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products
    WHERE product_id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product


def get_user_cart_id(chat_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id = (SELECT user_id FROM users WHERE telegram_id = ?)
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def insert_or_update_cart_product(cart_id, product, quantity, final_price):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?, ?, ?, ?)
        ''', (cart_id, product, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, final_price, product, cart_id))
        database.commit()
        return False
    finally:
        database.close()


def update_total_product_total_price(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts
    SET total_products = (
    SELECT SUM(quantity) FROM cart_products
    WHERE cart_id = :cart_id
    ),
    total_price = (
    SELECT SUM(final_price) FROM cart_products
    WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_cart_products(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def get_total_products_price(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()  # (5, 102000)
    database.close()
    return total_products, total_price


def get_cart_product_for_delete(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def delete_cart_product_from_database(cart_product_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products WHERE cart_product_id = ?
    ''', (cart_product_id,))
    database.commit()
    database.close()


def drop_cart_products_default(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    database.commit()
    database.close()


def orders_check():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_check(
        order_check_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0,
        time_order TEXT,
        date_order TEXT
        );
        ''')
    database.commit()
    database.close()


# orders_check()


def order():
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_check_id INTEGER REFERENCES orders_check(order_check_id),
        product_name VARCHAR(100) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL
    );
    ''')
    database.commit()
    database.close()


# order()


def save_order_check(cart_id, total_products, total_price, time_order, date_order):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders_check(cart_id, total_products, total_price, time_order, date_order)
    VALUES(?, ?, ?, ?, ?)
    ''', (cart_id, total_products, total_price, time_order, date_order))
    database.commit()
    database.close()


def save_order(order_check_id, product_name, quantity, final_price):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders(order_check_id, product_name, quantity, final_price)
    VALUES(?, ?, ?, ?)
    ''', (order_check_id, product_name, quantity, final_price))
    database.commit()
    database.close()


def get_order_check(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM orders_check
    WHERE cart_id = ?
    ''', (cart_id,))
    order_check_info = cursor.fetchall()
    database.close()
    return order_check_info


def get_detail_order(id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT product_name, quantity, final_price FROM orders
        WHERE order_check_id = ?
    ''', (id,))
    detail_order = cursor.fetchall()
    database.close()
    return detail_order

def get_order_check_id(cart_id):
    database = sqlite3.connect('burgercha.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT order_check_id FROM orders_check
    WHERE cart_id = ?
    ''', (cart_id,))
    order_check_id = cursor.fetchall()[-1][0]
    database.close()
    return order_check_id


