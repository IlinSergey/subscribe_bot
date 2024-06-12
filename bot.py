import asyncio

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers import subscribe_handlers, user_handlers


async def main() -> None:

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(bot=bot)

    dp.include_router(user_handlers.router)
    dp.include_router(subscribe_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
