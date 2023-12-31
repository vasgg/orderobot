from collections import namedtuple
from typing import Literal, NamedTuple, Union
from urllib.parse import urlparse

from aiogram import types
from aiogram.fsm.context import FSMContext
import arrow
from sqlalchemy import Result, delete, select, update

from core.config import settings, valid_domains
from core.database.models import Application, Order, User
from core.resources.dict import answer
from core.resources.enums import OrderStatus, UserType


async def send_order_text_to_channel(call: types.CallbackQuery, order_id: int, session) -> None:
    order = await get_order(order_id, session)
    await call.bot.send_message(
        chat_id=settings.CHANNEL_ID,
        text=answer["post_order"].format(
            order.id, order.name, order.budget, order.link, order.description
        ),
    )


async def send_order_text_to_customer(
    call: types.CallbackQuery,
    order: Order,
    mode: Literal['edit', 'answer'],
    state: FSMContext,
    markup: types.InlineKeyboardMarkup,
) -> None:
    match mode:
        case 'edit':
            await call.message.edit_text(
                text=answer['order_reply'].format(order.name, order.budget, order.link, order.description)
                + answer['order_reply_tail'],
                reply_markup=markup,
            )
        case 'answer':
            text = answer["publish_order_reply"] + answer["post_order"].format(
                order.id, order.name, order.budget, order.link, order.description)
            msg = await call.message.answer(text=text, reply_markup=markup)
            await state.update_data(published_message_id=msg.message_id)
    await call.answer()


def check_order_before_publish(order: Order) -> Union[bool, NamedTuple]:
    name = order.name != 'Безымянный заказ'
    budget = order.budget != '0'
    description = order.description != '—'
    Conditions = namedtuple('Conditions', ['название', 'бюджет', 'описание'])
    conditions = Conditions(название=name, бюджет=budget, описание=description)
    if all(conditions):
        return True
    else:
        return conditions


async def publish_order_to_db(order: Order, user: User, session) -> None:
    update_order = (
        update(Order)
        .filter(Order.customer_id == user.id, Order.status == OrderStatus.DRAFT)
        .values(
            name=order.name,
            budget=order.budget,
            description=order.description,
            link=order.link,
            status=OrderStatus.PUBLISHED,
        )
    )
    await session.execute(update_order)


def validate_url(url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.scheme == '':
        parsed_url = urlparse('http://' + url)
    domain = parsed_url.netloc
    return any(domain.endswith(valid_domain) for valid_domain in valid_domains)


async def get_order(order_id: int, session) -> Order:
    query = select(Order).filter(Order.id == order_id)
    result: Result = await session.execute(query)
    order = result.scalar()
    return order


async def get_user(user_id: int, session) -> User:
    query = select(User).filter(User.id == user_id)
    result: Result = await session.execute(query)
    user = result.scalar()
    return user


async def get_orders(
    session,
    user_id: int,
    mode: Literal['all', 'my', 'others', 'witout_worker'],
    status: OrderStatus,
) -> list[Order]:
    match mode:
        case 'all':
            query = select(Order).filter(Order.customer_id == user_id)
        case "my":
            query = select(Order).filter(Order.customer_id == user_id, Order.status == status)
        case 'others':
            query = select(Order).filter(Order.customer_id != user_id, Order.status == status)
        case _:
            raise ValueError(f'Unknown mode: {mode}')
    result = await session.execute(query)
    orders = result.scalars().all()
    return orders


async def create_draft(user_id: int, session) -> Order:
    new_draft = Order(customer_id=user_id)
    session.add(new_draft)
    await session.flush()
    query = select(Order).filter(Order.customer_id == user_id, Order.status == OrderStatus.DRAFT)
    result: Result = await session.execute(query)
    created_draft = result.scalar()
    return created_draft


async def get_customer_draft(user_id: int, session) -> Order:
    query = select(Order).filter(Order.customer_id == user_id, Order.status == OrderStatus.DRAFT)
    result: Result = await session.execute(query)
    draft = result.scalar()
    if not draft:
        draft = await create_draft(user_id, session)
    return draft


async def delete_draft(user_id: int, session) -> None:
    query = delete(Order).filter(Order.customer_id == user_id, Order.status == OrderStatus.DRAFT)
    await session.execute(query)


async def delete_published_order(order_id: int, session) -> None:
    query = delete(Order).filter(Order.id == order_id)
    await session.execute(query)


async def save_params_to_draft(
    order_id: int,
    mode: Literal['name', 'budget', 'description', 'link'],
    value: str,
    session,
) -> None:
    match mode:
        case "name":
            order = update(Order).filter(Order.id == order_id).values(name=value)
        case "budget":
            order = update(Order).filter(Order.id == order_id).values(budget=value)
        case "description":
            order = update(Order).filter(Order.id == order_id).values(description=value)
        case "link":
            order = update(Order).filter(Order.id == order_id).values(link=value)
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    await session.execute(order)


def get_unapplied_orders(
    user_id: int, orders: list[Order], applications: list[Application]
) -> list:
    orders_dict = {order.id: order for order in orders}
    for appl in applications:
        if appl.freelancer_id != user_id:
            continue
        del orders_dict[appl.order_id]
    return list(orders_dict.keys())


def get_orders_list_string(
    orders: list, mode: Literal['freelancer', 'customer']
) -> str:
    text = ''
    for order in sorted(orders, key=lambda x: x.id, reverse=True):
        created_at = arrow.get(order.created_at)
        match mode:
            case 'freelancer':
                text += (
                    f"🌐 id{order.id} · <b>{order.name}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 {order.budget}₽ · <i>бюджет проекта</i>\n\n"
                )
            case 'customer':
                text += f"🌐 id{order.id} · <b>{order.name}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n\n"
    if len(text) == 0:
        text = "🌐 Пока нет активных заказов"
    return text


async def add_worker_to_order(order_id: int, worker_id: int, session) -> None:
    query = update(Order).filter(Order.id == order_id).values(worker_id=worker_id)
    await session.execute(query)


async def get_active_orders(session, mode: UserType, worker_id: int = None, customer_id: int = None) -> list[Order]:
    match mode:
        case UserType.CUSTOMER:
            query = select(Order).filter(Order.customer_id == customer_id,
                                         Order.worker_id.is_not(None),
                                         Order.status != OrderStatus.DONE)
        case UserType.FREELANCER:
            query = select(Order).filter(Order.worker_id == worker_id,
                                         Order.status != OrderStatus.DONE)
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    result = await session.execute(query)
    orders = result.scalars().all()
    return orders


def check_balance_before_apply_worker(application_fee: int, user_balance: int) -> bool:
    if user_balance < application_fee:
        return False
    return True
