import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from data_base.db import Base
from handlers import profile_handlers, subscribe_handlers, user_handlers


async def main() -> None:

    Base.metadata.create_all(bind=Base.engine)

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot)

    dp.include_router(user_handlers.router)
    dp.include_router(profile_handlers.router)
    dp.include_router(subscribe_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
