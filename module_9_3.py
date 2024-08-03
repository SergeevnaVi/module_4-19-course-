first = ['Strings', 'Student', 'Computers']
second = ['Строка', 'Урбан', 'Компьютер']


first_result = (len(x) - len(y) for x, y in zip(first, second) if len(x) != len(y))

# Используем min(), чтобы в случае разной длины списка, избежать выхода за его пределы и не получать ошибок
second_result = (len(first[i]) == len(second[i]) for i in range(min(len(first), len(second))))

print(list(first_result))
print(list(second_result))

