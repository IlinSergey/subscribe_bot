import datetime
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError as TelegramError
from sqlalchemy import select

from config_data.config import Config, load_config
from data_base.db import Base
from data_base.models import User
from keyboards.main_menu import get_subscribe_menu
from lexicon.lexicon import LEXICON_RU

config: Config = load_config()


async def check_subscription(bot: Bot) -> None:
    """
    Checks the subscription status of all users in the database and bans any inactive users.
+
    Args:
        bot (Bot): The Telegram bot instance.

    Returns:
        None
    """
    result = await Base.db_session.execute(select(User))
    await Base.db_session.commit()
    users = result.scalars().all()
    admins = await check_admins(bot)
    for user in users:
        if user.tg_user_id not in admins:
            if not user.is_subscription_active() and not user.banned:
                try:
                    await bot.ban_chat_member(chat_id=config.channel_id.channel_id, user_id=user.tg_user_id)
                    user.banned = True
                    await Base.db_session.commit()
                    logging.info(f'User {user.tg_user_id} was banned')
                except TelegramError as err:
                    logging.error(err)


async def unban_user(bot: Bot, user_id: int) -> None:
    """
    Unbans a user from a Telegram chat.

    Args:
        bot (Bot): The Telegram bot instance.
        user_id (int): The ID of the user to unban.

    Returns:
        None

    Raises:
        TelegramError: If there is an error unbanning the user.
    """
    try:
        await bot.unban_chat_member(chat_id=config.channel_id.channel_id, user_id=user_id)
    except TelegramError as err:
        logging.error(err)


async def check_admins(bot: Bot) -> list[int]:
    """
    Retrieves a list of admin IDs from a Telegram chat.

    Args:
        bot (Bot): The Telegram bot instance.

    Returns:
        list[int]: A list of admin IDs.
    """
    admins = await bot.get_chat_administrators(chat_id=config.channel_id.channel_id)
    return [admin.user.id for admin in admins]


async def subscribe_renewal_reminder(bot: Bot, expire: int = 1) -> None:
    """
    Sends a subscription renewal reminder to all users who are not banned and their subscription is about to expire.

    Args:
        bot (Bot): The Telegram bot instance.

    Returns:
        None
    """
    result = await Base.db_session.execute(select(User))
    await Base.db_session.commit()
    users = result.scalars().all()
    current_date = datetime.datetime.now().date()
    for user in users:
        if not user.banned:
            sub_end_date = user.subscription_end_date
            if sub_end_date:
                time_difference = sub_end_date.date() - current_date
                if time_difference.days == expire:
                    try:
                        await bot.send_message(
                            chat_id=user.tg_user_id,
                            text=LEXICON_RU['sub_remind'],
                            reply_markup=await get_subscribe_menu())
                    except TelegramError as err:
                        logging.error(err)
