from aiogram.types import User as TgUser
from sqlalchemy import select

from data_base.db import Base
from data_base.models import User


async def get_user(tg_user_id: int) -> User | None:
    """
    Retrieve a user from the database based on the provided 'tg_user_id'.

    Parameters:
        tg_user_id (int): The Telegram user ID to search for.

    Returns:
        User or None: The user with the specified 'tg_user_id' or None if not found.
    """
    result = await Base.db_session.execute(select(User).where(User.tg_user_id == tg_user_id))
    await Base.db_session.commit()
    result = result.scalars().first()
    return result


async def create_user(tg_user: TgUser) -> None:
    """
    Create a new user in the database based on the provided 'tg_user'.

    Parameters:
        tg_user (TgUser): The Telegram user object containing user information.

    Returns:
        None
    """
    user = User(
        tg_user_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name
    )
    Base.db_session.add(user)
    await Base.db_session.commit()
