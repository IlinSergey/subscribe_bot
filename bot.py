import asyncio
import contextlib
import logging

import sentry_sdk
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger

from config_data.config import Config, load_config
from data_base.db import Base
from handlers import channel_handlers, subscribe_handlers, user_handlers
from middlewares.check_chat_id import CheckChatIdMiddleware
from middlewares.check_user_in_db import CheckUserInDBMiddleware
from services.subscribe_control import check_subscription, subscribe_renewal_reminder


async def main() -> None:

    async with Base.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    config: Config = load_config()

    sentry_sdk.init(config.sentry.dsn, traces_sample_rate=1.0, profiles_sample_rate=1.0)

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot)

    dp.message.middleware(CheckChatIdMiddleware())
    dp.message.middleware(CheckUserInDBMiddleware())

    dp.include_router(channel_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(subscribe_handlers.router)

    executor = ThreadPoolExecutor(max_workers=10)
    scheduler = AsyncIOScheduler(executor=executor)
    scheduler.add_job(check_subscription, IntervalTrigger(minutes=1), args=[bot])
    scheduler.add_job(subscribe_renewal_reminder, IntervalTrigger(minutes=1), args=[bot])

    scheduler.start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as err:
        logging.error(err)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        with contextlib.suppress(KeyboardInterrupt, SystemExit):
            logging.basicConfig(level=logging.WARNING, filename='bot.log',
                                filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
            asyncio.run(main())
    except Exception as err:
        logging.error(err)
        sentry_sdk.capture_exception(err)
