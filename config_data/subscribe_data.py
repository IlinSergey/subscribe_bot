from dataclasses import dataclass

from aiogram.types.labeled_price import LabeledPrice


@dataclass
class SubscribeInfo:
    description: str
    payload: str
    prices: list[LabeledPrice]


month_sub = SubscribeInfo(
    description='Подписка на месяц',
    payload='month_sub',
    prices=[
        LabeledPrice(label='rub', amount=15000),
    ]
)

year_sub = SubscribeInfo(
    description='Подписка на год',
    payload='year_sub',
    prices=[
        LabeledPrice(label='rub', amount=150000),
    ]
)
