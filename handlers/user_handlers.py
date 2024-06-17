from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from data_base.subscribe import get_end_date, get_subscription_status
from data_base.user import create_user, get_user
from keyboards.main_menu import get_main_menu
from lexicon.lexicon import LEXICON_RU

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    main_menu = await get_main_menu()
    if get_user(tg_user_id=message.from_user.id) is None:
        create_user(tg_user=message.from_user)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=main_menu)


@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'])


@router.message(F.text == 'ПРОФИЛЬ')
async def profile(message: Message) -> None:
    subscription_status = get_subscription_status(message.from_user.id)
    if subscription_status:
        end_date = get_end_date(message.from_user.id)
        await message.answer(f'✅ Ваша подписка заканчивается: {end_date}')
    else:
        await message.answer('❌ Ваша подписка неактивна')
