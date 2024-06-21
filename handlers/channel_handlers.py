from aiogram import Bot, Router
from aiogram.types import ChatJoinRequest

from config_data.config import Config, load_config
from data_base.subscribe import get_subscription_status
from handlers.subscribe_handlers import get_subscribe_menu
from lexicon.lexicon import LEXICON_RU

router: Router = Router()

config: Config = load_config()


@router.chat_join_request()
async def approve_request(chat_join: ChatJoinRequest, bot: Bot) -> None:
    if not await get_subscription_status(chat_join.from_user.id):
        await bot.send_message(
            chat_id=chat_join.from_user.id,
            text=LEXICON_RU['subscribe_nided'],
            reply_markup=await get_subscribe_menu()
            )
    else:
        await bot.send_message(
            chat_id=chat_join.from_user.id,
            text=LEXICON_RU['thanks']
            )
        await chat_join.approve()
