import datetime
import multiprocessing


def read_info(name):
    all_data = []
    with open(name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            all_data.append(line.strip())

filenames = [f'./file {number}.txt' for number in range(1, 5)]


# Линейный вызов
start = datetime.datetime.now()
for file in filenames:
    read_info(file)
end = datetime.datetime.now()
print(f'Время выполнения линейного вызова: {end - start}')


# Многопроцессный
start = datetime.datetime.now()
if __name__ == '__main__':
    with multiprocessing.Pool() as pool:
        pool.map(read_info, filenames)
    end = datetime.datetime.now()
    print(f'Время выполнения многопроцессного вызова: {end - start}')