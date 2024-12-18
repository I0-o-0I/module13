from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Информация'),
                                    KeyboardButton(text = 'Рассчитать')]],
                         resize_keyboard=True)
inkb = InlineKeyboardMarkup()
b = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
b2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
inkb.add(b)
inkb.add(b2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Информация о боте')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = inkb)

@dp.callback_query_handler(text = 'formulas')
async def formula(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = int(message.text))
    data = await state.get_data()

    a = 10 * data['weight'] + 6.25 + data['growth'] - 5 * data['age'] - 161
    await message.answer(f'Ваша норма калорий: {a}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)