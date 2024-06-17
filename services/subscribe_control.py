import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError as TelegramError

from config_data.config import Config, load_config
from data_base.db import Base
from data_base.models import User

config: Config = load_config()


def check_subscription(bot: Bot) -> None:
    users = Base.db_session.query(User).all()
    for user in users:
        if not user.is_subscription_active():
            try:
                bot.ban_chat_member(chat_id=config.channel_id.channel_id, user_id=user.tg_user_id)
                user.banned = True
                Base.db_session.commit()
                logging.info(f'User {user.tg_user_id} was banned')
            except TelegramError as err:
                logging.error(err)


def unban_user(bot: Bot, user_id: int) -> None:
    try:
        bot.unban_chat_member(chat_id=config.channel_id.channel_id, user_id=user_id)
    except TelegramError as err:
        logging.error(err)
