from aiogram import F, Router
from aiogram.types import Message

from data_base.subscribe import get_end_date, get_subscription_status

router: Router = Router()


@router.message(F.text == 'ПРОФИЛЬ')
async def profile(message: Message) -> None:
    subscription_status = get_subscription_status(message.from_user.id)
    if subscription_status:
        end_date = get_end_date(message.from_user.id)
        await message.answer(f'✅ Ваша подписка заканчивается: {end_date}')
    else:
        await message.answer('❌ Ваша подписка неактивна')
