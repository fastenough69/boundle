from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import Keyboards
from selector import NewAccount, Coockies
from database import DataBaseUsers
import functools
import asyncio


router = Router()
db = DataBaseUsers('users.db')

user_data = {}

class DataUser(StatesGroup):
    password = State()

class SetFirstCoockies(StatesGroup):
    first_coockies = State()

class NewCoockies(StatesGroup):
    coockies = State()
class FirstProxy(StatesGroup):
    first_proxy = State()

class NewProxy(StatesGroup):
    proxy_port = State()

class FirstPaste(StatesGroup):
    first_paste = State()

class NewPaste(StatesGroup):
    new_state = State()

def check_status(func):
    @functools.wraps(func)
    async def check(message: types.Message, state: FSMContext):
        if await db.get_status(message.from_user.id):
            args = [message, state]
            result = await func(*args)
            return result
        else:
            user_data[message.from_user.id] = {"first_name": message.from_user.first_name}
            await state.set_state(DataUser.password)
            await message.answer(f'Привет, {user_data[message.from_user.id]["first_name"]}, введите пароль')
    return check

@router.message(DataUser.password)
async def get_pass(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if await db.check_user(message.from_user.id, data["password"]):
        await db.set_status(message.from_user.id)
        await db.get_status(message.from_user.id)
        await message.answer(f'Вы успешно авторизовались', reply_markup=Keyboards.main)
        await state.clear()
    elif await db.check_user(message.from_user.id, data["password"]) is None:
        await message.answer('К сожелению вы не можете пользоваться моим функционалом')
        return
    else:
        await message.answer('Пароль не верный попробуйте еще раз')
        return

@router.message(CommandStart())
@check_status
async def start(message: types.Message, state: FSMContext):
    from main_telethon import main
    user_data[message.from_user.id] = {"first_name": message.from_user.first_name}
    await main(6367438515)
    await message.answer(f'Привет, {user_data[message.from_user.id]["first_name"]}', reply_markup=Keyboards.main)

@router.message(Command('settings'))
@check_status
async def select_settings(message: types.Message, state: FSMContext):
    await message.answer('Что хотите изменить?', reply_markup=Keyboards.settings)

@router.callback_query(F.data == 'begin_work')
async def start_work(call: types.CallbackQuery, state: FSMContext):
        if user_data[call.from_user.id].get("status", False):
            await call.answer('Загрузка...')
            await call.message.answer('Начал работу')
        else:
            await call.answer('Загрузка...')
            coockies_obj = NewAccount(call.from_user.id)
            if coockies_obj.get_cookie() is not None:
                user_data[call.from_user.id]["coockies"] = coockies_obj
                await state.set_state(FirstProxy.first_proxy)
                await call.message.answer('Нужно задать настройки\nУкажите порт к прокси серверу')
            else:   
                await state.set_state(SetFirstCoockies.first_coockies)
                await call.answer('Загрузка...')
                await call.message.answer('Нужно задать настройки\nОтправьте мне coockies данные с аккаунта')

@router.message(SetFirstCoockies.first_coockies)
async def set_first_coockies(message: types.Message, state: FSMContext):
    await state.update_data(first_coockies=message.text)
    data = await state.get_data()
    coockies_first = Coockies(message.from_user.id, coockies_user=data["first_coockies"])
    if coockies_first.err:
        user_data[message.from_user.id]["coockies"] = coockies_first
        await state.clear()

        await state.set_state(FirstProxy.first_proxy)
        await message.answer('Данные установлены\nТеперь укажите порт к прокси серверу')
        
    else:
        await message.answer('Произошла ошибка при записи данных, попробуйте еще раз')
        return
    
@router.message(FirstProxy.first_proxy)
async def set_first_proxy(message: types.Message, state: FSMContext):
    await state.update_data(first_proxy=message.text)
    data = await state.get_data()
    user_data[message.from_user.id]["proxy"] = data["first_proxy"]
    await state.clear()
    await state.set_state(FirstPaste.first_paste)
    await message.answer('Настройка прокси сервера устанавлена\nОсталось установить пасту для отправки')

@router.message(FirstPaste.first_paste)
async def set_first_paste(message: types.Message, state: FSMContext):
    await state.update_data(first_paste=message.text)
    data = await state.get_data()
    user_data[message.from_user.id]["paste"] = data["first_paste"]

    await state.clear()
    user_data[message.from_user.id]["status"] = True
    await message.answer('Все данные установлены. Нажмите на кнопку чтобы начать работу', reply_markup=Keyboards.main)

@router.message(Command('new_adm'))
@check_status
async def add_new_adm(message: types.Message):
    await message.answer('')

# @router.callback_query(F.data == 'change_coockies')
# async def new_coockies(call: types.CallbackQuery, state: FSMContext):
#     await state.set_state(NewCoockies.coockies)
#     await call.answer('Загрузка...')
#     await call.message.answer('Отправьте мне cookies данные с нового аккаунта')

# @router.message(NewCoockies.coockies)
# async def set_new_coockies(message: types.Message, state: FSMContext):
#     await state.update_data(coockies_new = message.text)
#     data = await state.get_data()
#     coockies_obj = Coockies(user_id=message.from_user.id, coockies_user=data["coockies_new"])
#     coockies_obj.write_coockies()
#     if coockies_obj.err:
#         user_data[message.from_user.id]["coockies"] = coockies_obj
#         await message.answer('Данные установлены можно продолжать работу', reply_markup=Keyboards.main)
#         await state.clear()
#     else:
#         await message.answer('Произошла ошибка при записи данных, попробуйте еще раз')
#         return

@router.callback_query(F.data == 'change_proxy')
async def new_proxy_port(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewProxy.proxy_port)
    await call.answer('Загрузка...')
    await call.message.answer('Укажите порт к прокси серверу')

@router.message(NewProxy.proxy_port)
async def set_proxy_port(message: types.Message, state: FSMContext):
    await state.update_data(new_port=message.text)
    data = await state.get_data()

    user_data[message.from_user.id]["proxy"] = data["new_port"]
    await message.answer('Настройка прокси сервера устанавлена, можно продолжать работу', reply_markup=Keyboards.main)

    await state.clear()

@router.callback_query(F.data == 'change_paste')
async def new_paste(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(NewPaste.new_state)
    await call.answer('Загрузка...')
    await call.message.answer('Отправте мне новую пасту')

@router.message(NewPaste.new_state)
async def set_new_paste(message: types.Message, state: FSMContext):
    await state.update_data(new_paste=message.text)
    data = await state.get_data()
    user_data[message.from_user.id]["paste"] = data["new_paste"]

    await message.answer('Паста установлна можно продолжать работу', reply_markup=Keyboards.main)

@router.message(Command('stop'))
async def end_job(message: types.Message):
    user_data[message.from_user.id]["status"] = False
    await message.answer(f'{user_data[message.from_user.id]["first_name"]}, вы завершили работу!')