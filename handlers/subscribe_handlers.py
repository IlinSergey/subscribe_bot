from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery

import config_data.subscribe_data as subscribe_data
from config_data.config import load_config
from data_base.subscribe import (create_subscription, get_subscription_status,
                                 renew_subscription)
from data_base.user import get_user
from keyboards.main_menu import get_main_menu, get_subscribe_menu
from services.subscribe_control import unban_user

config = load_config()


router: Router = Router()


@router.message(F.text == 'ПОДПИСКА')
async def subscribe(message: Message) -> None:
    subscribe_menu = await get_subscribe_menu()
    if await get_subscription_status(message.from_user.id):
        await message.answer(text='Выберите на какой срок продлить действующею подписку:', reply_markup=subscribe_menu)
    else:
        await message.answer(text='Варианты подписки:', reply_markup=subscribe_menu)


@router.callback_query((F.data == 'sub_month') | (F.data == 'sub_year'))
async def callback_query_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    match callback.data:
        case 'sub_month':
            await send_invoice(callback=callback,
                               bot=callback.bot,  # type: ignore
                               subscribe_info=subscribe_data.month_sub,
                               )
        case 'sub_year':
            await send_invoice(callback=callback,
                               bot=callback.bot,  # type: ignore
                               subscribe_info=subscribe_data.year_sub)


async def send_invoice(callback: CallbackQuery,
                       bot: Bot,
                       subscribe_info: subscribe_data.SubscribeInfo) -> None:
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Подписка',
        description=subscribe_info.description,
        payload=subscribe_info.payload,
        provider_token=config.yookassa.secret_key,
        currency='rub',
        start_parameter='subscribe-invoice-sender',
        prices=subscribe_info.prices,
    )


@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message()
async def successful_payment(message: Message, bot: Bot) -> None:
    user = await get_user(tg_user_id=message.from_user.id)
    is_subscribed = user.is_subscription_active()
    keyboard = await get_main_menu()
    if user.banned:
        await unban_user(bot=bot, user_id=message.from_user.id)
    match message.successful_payment.invoice_payload:
        case 'month_sub':
            if is_subscribed:
                await renew_subscription(tg_user_id=message.from_user.id, duration=30)
                await message.answer(text='Продлена подписка на месяц', reply_markup=keyboard)
                await message.delete()
            else:
                await create_subscription(tg_user_id=message.from_user.id, duration=30)
                await message.answer(text='Оформлена подписка на месяц', reply_markup=keyboard)
                await message.delete()
        case 'year_sub':
            if is_subscribed:
                await renew_subscription(tg_user_id=message.from_user.id, duration=365)
                await message.answer(text='Продлена подписка на год', reply_markup=keyboard)
                await message.delete()
            else:
                await create_subscription(tg_user_id=message.from_user.id, duration=365)
                await message.answer(text='Оформлена подписка на год', reply_markup=keyboard)
                await message.delete()
        case _:
            await message.answer(text='Оплата прошла успешно', reply_markup=keyboard)
            await message.delete()
