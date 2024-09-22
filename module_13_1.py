import asyncio
import time

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for i in range(1, 6):
        await asyncio.sleep(power)
        print(f'Силач {name} поднял {i} шар!')
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Ivan', 5))
    task2 = asyncio.create_task(start_strongman('Denis', 3))
    task3 = asyncio.create_task(start_strongman('Misha', 4))
    await task1
    await task2
    await task3

start = time.time()
asyncio.run(start_tournament())
end = time.time()
print(f'Время работы = {round(end-start, 2)} секунд')
