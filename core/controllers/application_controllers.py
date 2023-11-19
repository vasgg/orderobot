from typing import Literal

from aiogram import types
import arrow
from sqlalchemy import Result, delete, select

from core.database.models import Application


# def get_user(user_id: int, session) -> User:
#     # noinspection PyUnresolvedReferences
#     user = (
#         session.query(User)
#         .options(selectinload(User.orders_as_worker))
#         .filter(User.id == user_id)
#         .first()
#     )
#     return user
#
#
# def get_order(order_id: int, session) -> Order:
#     order = (
#         session.query(Order)
#         .options(joinedload(Order.worker))
#         .filter(Order.id == order_id)
#         .first()
#     )
#     return order
#
#
# def get_applications(user_id: int, session) -> list[Application]:
#     applications = (
#         session.query(Application)
#         .options(joinedload(Application.freelancer), joinedload(Application.order))
#         .filter(Application.freelancer_id == user_id)
#         .all()
#     )
#     return applications
async def create_application(
    order_id: int,
    customer_id: int,
    freelancer_id: int,
    fee: int,
    completion_days: int,
    message: str,
    session,
) -> None:
    new_application = Application(
        order_id=order_id,
        customer_id=customer_id,
        freelancer_id=freelancer_id,
        fee=fee,
        completion_days=completion_days,
        message=message,
    )
    session.add(new_application)


async def get_applications(
    session,
    mode: Literal['all', 'by_customer', 'by_worker', 'by_order'],
    customer_id: int = None,
    worker_id: int = None,
    order_id: int = None,
) -> list[Application]:
    match mode:
        case 'all':
            query = select(Application)
        case 'by_customer':
            query = select(Application).filter(Application.customer_id == customer_id)
        case 'by_worker':
            query = select(Application).filter(Application.freelancer_id == worker_id)
        case 'by_order':
            query = select(Application).filter(Application.order_id == order_id)
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    result = await session.execute(query)
    applications = result.scalars().all()
    return applications


async def get_application(application_id: int, session) -> Application:
    query = select(Application).filter(Application.id == application_id)
    result: Result = await session.execute(query)
    application = result.scalar()
    return application


def get_applications_list_string(
    applications: list, mode: Literal['freelancer', 'customer'], orders: list = None
) -> str:
    text = ''
    orders_dict = {order.id: order for order in orders}
    for application in sorted(applications, key=lambda x: x.id, reverse=True):
        created_at = arrow.get(application.created_at)
        match mode:
            case 'freelancer':
                text += (
                    f"🔼 <b>Заявка id{application.id}</b> · <i>создана {created_at.humanize(locale='ru')}</i>\n"
                    f"🌐 к заказу <b>id{application.order_id} · {orders_dict[application.order_id].name}</b>\n"
                    f"💎 <b>{application.fee}₽</b> · <i>стоимость работы</i>\n"
                    f"⏳ <b>{application.completion_days}</b> · <i>срок выполнения в днях</i>\n\n"
                )
            case 'customer':
                assert orders is not None
                text += (
                    f"🔼 <b>Заявка id{application.id}</b> к вашему заказу <b>id{application.order_id}</b>\n"
                    f"🌐 <b>{orders_dict[application.order_id].name}</b> · "
                    f"<i>Бюджет</i> <b>{orders_dict[application.order_id].budget}₽</b>\n"
                    f"🕛 <i>созданa {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 <i>стоимость работы</i> · <b>{application.fee}₽</b>\n"
                    f"⏳ <i>срок выполнения в днях</i> · <b>{application.completion_days}</b>\n"
                    f"📝 <i>сообщение</i> · <b>{application.message}</b>\n\n"
                )
            case _:
                raise ValueError(f"Unknown mode: {mode}")
    if len(text) == 0:
        text = "🌐 Пока нет активных заявок"
    return text


async def del_application(application_id: int, session) -> None:
    query = delete(Application).filter(Application.id == application_id)
    await session.execute(query)


async def send_message(message: types.Message, receiver_id: int, text: str, reply_markup: types.InlineKeyboardMarkup) -> None:
    await message.bot.send_message(chat_id=receiver_id,
                                   text=text,
                                   reply_markup=reply_markup)
