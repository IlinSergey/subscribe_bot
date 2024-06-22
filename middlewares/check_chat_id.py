from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config_data.config import Config, load_config

config: Config = load_config()


class CheckChatIdMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        if event.chat.id != config.channel_id.channel_id:
            await handler(event, data)
        else:
            await handler(event, data)
