from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *


initiate_db()

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Купить')
        ],
        [
            KeyboardButton(text='Регистрация')
        ]
    ], resize_keyboard=True
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формула расчета', callback_data='formulas')]
    ], row_width=2
)

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product 1 - Vanilla', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product 2 - Strawberry', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product 3 - Chocolate', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product 4 - Tropic', callback_data='product_buying')]
    ]
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=start_menu)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.message_handler(text='Информация')
async def main_menu(message):
    await message.answer('В нашем магазине протеинов вы найдете качественные добавки для достижения ваших фитнес-целей\n'
                         '\nДоставка от 3000 рублей - бесплатная!')

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    for i, product in enumerate(products, start=1):
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]} рублей')
        try:
            with open(f"pictures/{i}.jpg", "rb") as img:
                await message.answer_photo(img)
        except FileNotFoundError:
            await message.answer(f'Картинка для продукта {product[1]} недоступна')
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_menu)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()



class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    add_user(**data)
    await message.answer('Вы успешно зарегистрированы!')
    await state.finish()



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()  # добавила свое

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
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