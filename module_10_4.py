import threading
from queue import Queue
from random import randint
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        amount = randint(3,10)
        sleep(amount)


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables
        self.lock = threading.Lock()

    def guest_arrival(self, *guests):
        for guest in guests:
            with self.lock:
                available_table = None
                for table in self.tables:
                    if table.guest is None:
                        available_table = table
                        break

                if available_table:
                    available_table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {available_table.number}')
                else:
                    self.queue.put(guest)
                    print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            with self.lock:
                for table in self.tables:
                    if table.guest is not None and not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None

                        if not self.queue.empty():
                            next_guest = self.queue.get()
                            table.guest = next_guest
                            next_guest.start()
                            print(f'{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')




# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()