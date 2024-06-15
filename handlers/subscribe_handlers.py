from aiogram import Bot, F, Router
from aiogram.types import (CallbackQuery, ChatJoinRequest, Message,
                           PreCheckoutQuery)

import config_data.subscribe_data as subscribe_data
from config_data.config import load_config
from data_base.subscribe import (create_subscription, get_subscription_status,
                                 renew_subscription)
from keyboards.main_menu import get_main_menu, get_subscribe_menu
from lexicon.lexicon import LEXICON_RU

config = load_config()


router: Router = Router()


@router.message(F.text == 'ПОДПИСКА')
async def subscribe(message: Message) -> None:
    subscribe_menu = await get_subscribe_menu()
    if get_subscription_status(message.from_user.id):
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
async def successful_payment(message: Message) -> None:
    is_subscribed = get_subscription_status(message.from_user.id)
    keyboard = get_main_menu()
    match message.successful_payment.invoice_payload:
        case 'month_sub':
            if is_subscribed:
                renew_subscription(tg_user_id=message.from_user.id, duration=30)
                await message.answer(text='Продлена подписка на месяц', reply_markup=keyboard)
            else:
                create_subscription(tg_user_id=message.from_user.id, duration=30)
                await message.answer(text='Оформлена подписка на месяц', reply_markup=keyboard)
        case 'year_sub':
            if is_subscribed:
                renew_subscription(tg_user_id=message.from_user.id, duration=365)
                await message.answer(text='Продлена подписка на год', reply_markup=keyboard)
            else:
                create_subscription(tg_user_id=message.from_user.id, duration=365)
                await message.answer(text='Оформлена подписка на год', reply_markup=keyboard)
        case _:
            await message.answer(text='Оплата прошла успешно', reply_markup=keyboard)


@router.chat_join_request(F.chat.id == config.channel_id.channel_id)
async def approve_request(chat_join: ChatJoinRequest, bot: Bot) -> None:
    if not get_subscription_status(chat_join.from_user.id):
        await bot.send_message(
            chat_id=chat_join.from_user.id,
            text=LEXICON_RU['subscribe_nided'],
            reply_markup=await get_subscribe_menu()
            )
    else:
        await bot.send_message(
            chat_id=chat_join.from_user.id,
            text=LEXICON_RU['thanks']
            )
        await chat_join.approve()
