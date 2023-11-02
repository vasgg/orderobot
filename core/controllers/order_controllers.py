from collections import namedtuple
from typing import Literal, NamedTuple, Union
from urllib.parse import urlparse

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
import arrow
from sqlalchemy import update

from core.config import channel, valid_domains
from core.database.db import db
from core.database.models import Application, Order, User

from core.resources.dictionaries import answer


async def send_order_text_to_channel(bot: Bot, order_id: int, session) -> None:
    order = get_order(order_id, session)
    await bot.send_message(
        chat_id=channel,
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
                text=answer['order_reply'].format(
                    order.name, order.budget, order.link, order.description
                )
                + answer['order_reply_tail'],
                reply_markup=markup,
            )
        case 'answer':
            text = answer["publish_order_reply"] + answer["post_order"].format(
                order.id, order.name, order.budget, order.link, order.description
            )
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
        .where(Order.customer_id == user.id, Order.status == 'draft')
        .values(
            name=order.name,
            budget=order.budget,
            description=order.description,
            link=order.link,
            status='published',
        )
    )
    session.execute(update_order)


def validate_url(url: str) -> bool:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return any(domain.endswith(valid_domain) for valid_domain in valid_domains)


def get_order(order_id: int, session) -> Order:
    order = session.query(Order).filter(Order.id == order_id).first()
    return order


def get_user(user_id: int, session) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    return user


def get_orders(
    session,
    user_id: int,
    mode: Literal['all', 'my', 'others'],
    status: Literal[
        'draft',
        'published',
        'WIP',
        'completed',
    ],
) -> list[Order]:
    match mode:
        case 'all':
            orders = session.query(Order).where(Order.status == status).all()
        case "my":
            orders = (
                session.query(Order)
                .where(Order.customer_id == user_id, Order.status == status)
                .all()
            )
        case 'others':
            orders = (
                session.query(Order)
                .join(Application)
                .where(
                    Order.customer_id != user_id,
                    Order.status == status,
                    Application.freelancer_id != user_id,
                ).all()
            )
        case _:
            raise ValueError(f'Unknown mode: {mode}')
    return orders


def create_draft(user_id: int, session) -> Order:
    new_draft = Order(
        customer_id=user_id,
    )
    session.add(new_draft)
    session.commit()
    with db.session.begin() as session:
        created_draft = (
            session.query(Order)
            .filter(Order.customer_id == user_id, Order.status == 'draft')
            .first()
        )
    return created_draft


def get_customer_draft(user_id: int) -> Order:
    with db.session.begin() as session:
        draft = (
            session.query(Order)
            .filter(Order.customer_id == user_id, Order.status == 'draft')
            .first()
        )
        if not draft:
            draft = create_draft(user_id, session)
        return draft


def delete_draft(user_id: int) -> None:
    with db.session.begin() as session:
        session.query(Order).filter(
            Order.customer_id == user_id, Order.status == 'draft'
        ).delete()


def delete_published_order(order_id: int) -> None:
    with db.session.begin() as session:
        session.query(Order).filter(Order.id == order_id).delete()


def save_params_to_draft(
    order_id: int, mode: Literal['name', 'budget', 'description', 'link'], value: str
) -> None:
    with db.session.begin() as session:
        match mode:
            case "name":
                order = update(Order).where(Order.id == order_id).values(name=value)
            case "budget":
                order = update(Order).where(Order.id == order_id).values(budget=value)
            case "description":
                order = (
                    update(Order).where(Order.id == order_id).values(description=value)
                )
            case "link":
                order = update(Order).where(Order.id == order_id).values(link=value)
        session.execute(order)


def get_unapplied_orders(user_id: int, orders: list, applications: list) -> list:
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
                    f"🌐 <b>{order.name}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 {order.budget}₽ · <i>бюджет проекта</i>\n\n"
                )
            case 'customer':
                text += f"🌐 id{order.id} · <b>{order.name}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n\n"
    if len(text) == 0:
        text = "🌐 Пока нет активных заказов"
    return text
