from datetime import datetime
from typing import Literal

import arrow
from sqlalchemy import Result, select, update

from core.database.models import Order, User
from core.resources.enums import OrderStatus


async def create_user_in_db(event, session) -> User:
    new_user = User(
        telegram_id=event.from_user.id,
        username=event.from_user.username,
        fullname=event.from_user.full_name,
    )
    session.add(new_user)
    await session.flush()
    return new_user


async def get_user_from_db(event, session) -> User:
    query = select(User).filter(User.telegram_id == event.from_user.id)
    result: Result = await session.execute(query)
    user = result.scalar()
    if not user:
        user = await create_user_in_db(event, session)
    return user


async def get_deals_counter(
    user_id: int, mode: Literal['customer', 'freelancer'], session
) -> int:
    counter = 0
    match mode:
        case 'customer':
            query = select(Order).filter(
                Order.customer_id == user_id, Order.status == OrderStatus.DONE
            )
        case 'freelancer':
            query = select(Order).filter(
                Order.worker_id == user_id, Order.status == OrderStatus.DONE
            )
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    result = await session.execute(query)
    orders = result.scalars().all()
    if orders is not None:
        counter = len(orders)
    return counter


def get_time_since_registration(created_at: datetime) -> str:
    created_at = arrow.get(created_at)
    return created_at.humanize(locale='ru')


async def rename_user(telegram_id: int, new_username: str, session) -> None:
    new_name = (
        update(User)
        .filter(User.telegram_id == telegram_id)
        .values(fullname=new_username)
    )
    await session.execute(new_name)


async def change_user_balance(telegram_id: int, current_balance: int, amount: int, mode: Literal['add', 'subtract'], session) -> None:
    match mode:
        case 'add':
            new_balance = (
                update(User)
                .filter(User.telegram_id == telegram_id)
                .values(balance=current_balance + amount)
            )
        case 'subtract':
            new_balance = (
                update(User)
                .filter(User.telegram_id == telegram_id)
                .values(balance=current_balance - amount)
            )
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    await session.execute(new_balance)
