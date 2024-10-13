import sqlite3


def initiate_db():
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price INT NOT NULL
            );    
        ''')

        cursor.execute('SELECT COUNT(*) FROM Products')
        count = cursor.fetchone()[0]

        if count == 0:
            products = [
                ('Протеин 1', 'VANILLA', 1700),
                ('Протеин 2', 'STRAWBERRY', 1500),
                ('Протеин 3', 'CHOCOLATE', 2000),
                ('Протеин 4', 'TROPIC', 2200)
            ]
            cursor.executemany(
                'INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                    products
            )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL
            );
        """)

        connection.commit()

def get_all_products():
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT id, title, description, price FROM Products')
        products = cursor.fetchall()
    return products

def is_included(username):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM Users WHERE username = ?',
            (username,)
        )
        user = cursor.fetchone()
    return bool(user)


def add_user(username, email, age):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        if not is_included(username):
            cursor.execute(
                'INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)',
                (username, email, age, 1000)
            )
        connection.commit()
