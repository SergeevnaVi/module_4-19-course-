from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = 'api_key'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
start_menu.add(button1)
start_menu.add(button2)
start_menu.add(button3)

inline_keyboard = InlineKeyboardMarkup(row_width=2)
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
inline_keyboard.add(button4)
inline_keyboard.add(button5)


inline_menu = InlineKeyboardMarkup()
btn6 = InlineKeyboardButton(text='Product1 - Vanilla', callback_data='product_buying')
btn7 = InlineKeyboardButton(text='Product2 - Strawberry', callback_data='product_buying')
btn8 = InlineKeyboardButton(text='Product3 - Chocolate', callback_data='product_buying')
btn9 = InlineKeyboardButton(text='Product4 - Tropic', callback_data='product_buying')
inline_menu.add(btn6)
inline_menu.add(btn7)
inline_menu.add(btn8)
inline_menu.add(btn9)


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
    for i in range(1, 5):
        await message.answer(f'Название: Product{i} | Описание: protein{i} | Цена: {i*1000}')
        with open(f"pictures/{i}.jpg", "rb") as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_menu)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

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
