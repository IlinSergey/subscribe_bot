from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class ChannelID:
    channel_id: int


@dataclass
class YooKassa:
    secret_key: str


@dataclass
class DataBase:
    path: str


@dataclass
class Config:
    tg_bot: TgBot
    yookassa: YooKassa
    db: DataBase
    channel_id: ChannelID


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        yookassa=YooKassa(secret_key=env('YOOTOKEN')),
        db=DataBase(path=env('DB_PATH')),
        channel_id=ChannelID(channel_id=env('CHANNEL_ID'))
        )
