from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from data_base.user import create_user, get_user


class CheckUserInDBMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        if get_user(tg_user_id=event.from_user.id) is None:
            create_user(tg_user=event.from_user)
            await handler(event, data)
        else:
            await handler(event, data)
