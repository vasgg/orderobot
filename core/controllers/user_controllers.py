from datetime import datetime
from typing import Literal

import arrow
from sqlalchemy import update

from core.database.db import db
from core.database.models import Order, User


def create_user(event, session) -> User:
    new_user = User(
        telegram_id=event.from_user.id,
        username=event.from_user.username,
        fullname=event.from_user.full_name,
    )
    session.add(new_user)
    session.commit()
    with db.session.begin() as session:
        created_user = (
            session.query(User).filter(User.telegram_id == event.from_user.id).first()
        )
    return created_user


def get_user(event) -> User:
    with db.session.begin() as session:
        user = (
            session.query(User).filter(User.telegram_id == event.from_user.id).first()
        )
        if not user:
            user = create_user(event, session)
    return user


def get_deals(user_id: int, mode: Literal['customer', 'freelancer']) -> int:
    with db.session.begin() as session:
        match mode:
            case 'customer':
                counter = (
                    session.query(Order)
                    .where(Order.customer_id == user_id)
                    .filter(Order.status == 'done')
                    .count()
                )
                return counter
            case 'freelancer':
                counter = (
                    session.query(Order)
                    .where(Order.worker_id == user_id)
                    .filter(Order.status == 'done')
                    .count()
                )

                return counter


def get_time_since_registration(created_at: datetime) -> str:
    created_at = arrow.get(created_at)
    return created_at.humanize(locale='ru')


def rename_user(telegram_id: int, new_username: str) -> None:
    with db.session.begin() as session:
        new_name = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(fullname=new_username)
        )
        session.execute(new_name)
