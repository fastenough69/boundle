from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Начать работу', callback_data='begin_work')],
    ])

    settings = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text='Смена аккаунта', callback_data='change_coockies')],
        [InlineKeyboardButton(text='Смена прокси', callback_data='change_proxy')],
        [InlineKeyboardButton(text='Смена пасты', callback_data='change_paste')]
    ])