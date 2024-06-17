import asyncio
import contextlib
import logging
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config_data.config import Config, load_config
from data_base.db import Base
from handlers import channel_handlers, subscribe_handlers, user_handlers
from middlewares.check_user_in_db import CheckUserInDBMiddleware
from services.subscribe_control import check_subscription


async def main() -> None:

    Base.metadata.create_all(bind=Base.engine)

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot)

    dp.message.middleware(CheckUserInDBMiddleware())

    dp.include_router(user_handlers.router)
    dp.include_router(channel_handlers.router)
    dp.include_router(subscribe_handlers.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_subscription, IntervalTrigger(minutes=1), args=[bot])
    scheduler.start()

    check_subscription(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as err:
        logging.error(err)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
