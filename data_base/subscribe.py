from datetime import datetime, timedelta

from data_base.db import Base
from data_base.models import User


def create_subscription(tg_user_id: int, duration: int) -> None:
    """
    Create a subscription for the user with the specified 'tg_user_id' and the provided 'duration'.

    Parameters:
        tg_user_id (int): The Telegram user ID for whom the subscription is created.
        duration (int): The duration of the subscription in days.

    Returns:
        None
    """
    user = Base.db_session.query(User).filter(User.tg_user_id == tg_user_id).first()
    if user:
        user.subscription_start_date = datetime.now()
        user.subscription_end_date = datetime.now() + timedelta(days=duration)
        Base.db_session.commit()
    else:
        pass


def renew_subscription(tg_user_id: int, duration: int) -> None:
    """
    Renews a subscription for a user with the specified Telegram user ID.

    Args:
        tg_user_id (int): The Telegram user ID for whom the subscription is renewed.
        duration (int): The duration of the subscription in days.

    Returns:
        None: This function does not return anything.
    """
    user = Base.db_session.query(User).filter(User.tg_user_id == tg_user_id).first()
    if user:
        if user.subscription_end_date and user.subscription_end_date > datetime.now():
            user.subscription_end_date += timedelta(days=duration)
        else:
            user.subscription_start_date = datetime.now()
            user.subscription_end_date = datetime.now() + timedelta(days=duration)
        Base.db_session.commit()
    else:
        pass


def get_end_date(tg_user_id: int) -> str | None:
    """
    Get the end date of a subscription for a user with the specified Telegram user ID.

    Args:
        tg_user_id (int): The Telegram user ID for whom the subscription end date is requested.

    Returns:
        str | None: The end date of the subscription or None if the user has no subscription.
    """
    user = Base.db_session.query(User).filter(User.tg_user_id == tg_user_id).first()
    if user:
        if user.subscription_end_date:
            return user.subscription_end_date.date().strftime('%d.%m.%Y')
        else:
            return None
    else:
        return None


def get_subscription_status(tg_user_id: int) -> bool:
    """
    Get the subscription status of a user with the specified Telegram user ID.

    Args:
        tg_user_id (int): The Telegram user ID for whom the subscription status is requested.

    Returns:
        bool: True if the user has a subscription, False otherwise.
    """
    user = Base.db_session.query(User).filter(User.tg_user_id == tg_user_id).first()
    if user:
        if user.subscription_end_date and user.subscription_end_date > datetime.now():
            return True
        else:
            return False
    else:
        return False
