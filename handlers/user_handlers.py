from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.main_menu import get_main_menu
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    main_menu = await get_main_menu()
    await message.answer(text=LEXICON_RU['/start'], reply_markup=main_menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'])
