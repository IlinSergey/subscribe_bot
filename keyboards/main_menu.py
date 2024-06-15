from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


async def get_main_menu() -> ReplyKeyboardMarkup:
    btn_subscribe = KeyboardButton(text='ПОДПИСКА')
    btn_profile = KeyboardButton(text='ПРОФИЛЬ')
    main_menu = ReplyKeyboardMarkup(keyboard=[[btn_subscribe, btn_profile]], resize_keyboard=True)
    return main_menu


async def get_subscribe_menu() -> InlineKeyboardMarkup:
    btn_month_sub = InlineKeyboardButton(text='Месяц - 150₽', callback_data='sub_month')
    btn_year_sub = InlineKeyboardButton(text='Год - 1500₽', callback_data='sub_year')
    subscribe_menu = InlineKeyboardMarkup(
        inline_keyboard=[[btn_month_sub, btn_year_sub]], row_width=1
        )
    return subscribe_menu
