from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
keyboard.add(button)
keyboard.insert(button2)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=keyboard)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()  # добавила свое

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Укажите свой пол (мужчина/женщина):')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    gender = message.text.lower()
    if gender not in ['мужчина', 'женщина']:
        await message.answer('Пожалуйста, введите корректный пол: "мужчина" или "женщина"')
        return

    data = await state.get_data()

    age = int(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])

    if gender == 'женщина':
        # Формула для женщин
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
    else:
        # Формула для мужчин
        calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f'Ваша суточная норма калорий: {calories} калорий.')
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)