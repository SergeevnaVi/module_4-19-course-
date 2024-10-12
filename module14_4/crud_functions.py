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

        connection.commit()

def get_all_products():
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT id, title, description, price FROM Products')
        products = cursor.fetchall()
    return products
