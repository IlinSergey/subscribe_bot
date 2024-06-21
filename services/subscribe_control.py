import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError as TelegramError
from sqlalchemy import select

from config_data.config import Config, load_config
from data_base.db import Base
from data_base.models import User

config: Config = load_config()


async def check_subscription(bot: Bot) -> None:
    result = await Base.db_session.execute(select(User))
    users = result.scalars().all()
    for user in users:
        if not user.is_subscription_active() and not user.banned:
            try:
                await bot.ban_chat_member(chat_id=config.channel_id.channel_id, user_id=user.tg_user_id)
                user.banned = True
                await Base.db_session.commit()
                logging.info(f'User {user.tg_user_id} was banned')
            except TelegramError as err:
                logging.error(err)


async def unban_user(bot: Bot, user_id: int) -> None:
    try:
        await bot.unban_chat_member(chat_id=config.channel_id.channel_id, user_id=user_id)
    except TelegramError as err:
        logging.error(err)
