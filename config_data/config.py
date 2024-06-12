from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class YooKassa:
    secret_key: str


@dataclass
class Config:
    tg_bot: TgBot
    yookassa: YooKassa


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        yookassa=YooKassa(secret_key=env('YOOTOKEN')))
