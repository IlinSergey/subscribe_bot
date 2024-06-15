from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from data_base.user import create_user, get_user
from keyboards.main_menu import get_main_menu
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    main_menu = await get_main_menu()
    if get_user(tg_user_id=message.from_user.id) is None:
        create_user(tg_user=message.from_user)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=main_menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'])
