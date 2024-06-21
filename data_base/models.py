from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from data_base.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003 VNE003
    tg_user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    subscription_start_date: Mapped[datetime] = mapped_column(nullable=True)
    subscription_end_date: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    banned: Mapped[bool] = mapped_column(nullable=False, default=False)

    def is_subscription_active(self) -> bool:
        if self.subscription_end_date and self.subscription_end_date > datetime.now():
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f'User(id={self.tg_user_id}, username={self.username})'
