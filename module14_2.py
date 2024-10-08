import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Заполняем таблицу записями
for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'User{i}', f'example{i}@gmail.com', i*10, 1000))

# Обновляем balance у каждой 2ой записи начиная с 1ой на 500
cursor.execute(f'UPDATE Users SET balance = 500 WHERE id % 2 == 1')

# Удаляем каждую 3ую запись начиная с 1ой
cursor.execute('DELETE FROM Users WHERE id % 3 == 1')

# Удаляем запись с id = 6
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

# Считаем кол-во записей
cursor.execute('SELECT COUNT(*) FROM Users')
total = cursor.fetchone()[0]

# Считаем сумму всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
summa = cursor.fetchone()[0]

# Выводим средний баланс всех пользователей
print(summa / total)

connection.commit()
connection.close()
