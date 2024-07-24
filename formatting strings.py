# Использование %
team1_num = 5
print("В команде Мастера кода участников: %s!" % team1_num)
team2_num = 6
print("В команде Мастера кода участников: %s и %s!" % (team1_num, team2_num))


# Использование format()
score_2 = 42
print("Команда Волшебники данных решила задач: {}!".format(score_2))
team1_time = 18015.2
print("Волшебники данных решили задачи за {} с!".format(team1_time))


# Использование f-строк
score_1 = 40
print(f'Команды решили {score_1} и {score_2} задач.')
challenge_result = 'победа'
print(f'Результат битвы: {challenge_result} команды Мастера кода!')
tasks_total = 82
time_avg = 350.4
print(f'Сегодня было решено {tasks_total} задач, в среднем по {time_avg} секунды на задачу!')


# challenge_result
team2_time = 15022.5
if score_1 > score_2 or score_1 == score_2 and team1_time > team2_time:
    challenge_result = 'Победа команды Мастера кода!'
elif score_1 < score_2 or score_1 == score_2 and team1_time < team2_time:
    challenge_result = 'Победа команды Волшебники данных!'
else:
    challenge_result = 'Ничья!'
print(challenge_result)
