import time
import requests
import pandas as pd
import matplotlib.pyplot as plt


# Запрос данных о погоде в разных городах
api_key = '7b2a9f86c7b8cf985f24557f6ee25e21'
cities = ['Москва', 'Париж', 'Чикаго', 'Стамбул', 'Казань']
weather_data = []

for city in cities:
    for attempt in range(2):
        try:
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
            response.raise_for_status()
            data = response.json()
            weather_data.append({
                'Город': city,
                'Температура': data['main']['temp'],
                'Влажность': data['main']['humidity']
            })
            break
        except requests.exceptions.RequestException as e:
            print(f'Попытка {attempt + 1}: Не удалось получить данные для {city}')
            time.sleep(2)

# Преобразование данных в DataFrame и выполнение анализа
if weather_data:
    df = pd.DataFrame(weather_data)
    print('Данные о погоде:')
    print(df)

    mean_temp = df['Температура'].mean()
    mean_humidity = df['Влажность'].mean()
    print(f'Средняя температура: {mean_temp.round(1)}°C')
    print(f'Средняя влажность: {mean_humidity.round(1)}%')

    # Визуализация данных с помощью библиотеки Matplotlib
    plt.figure()
    plt.bar(df['Город'], df['Температура'], color='darkblue')
    plt.xlabel('Город')
    plt.ylabel('Температура (°C)')
    plt.title('Температура в разных городах')
    plt.show()
else:
    print("Не удалось получить данные ни для одного города.")


