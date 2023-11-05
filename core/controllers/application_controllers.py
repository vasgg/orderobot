from typing import Literal

from arrow import arrow

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
def create_application(order_id: int, customer_id: int, freelancer_id: int, session) -> None:
    new_application = Application(
        order_id=order_id,
        customer_id=customer_id,
        freelancer_id=freelancer_id,
    )
    session.add(new_application)


def get_applications(session, mode: Literal['all', 'by_customer', 'by_worker', 'by_order'], customer_id: int = None,
                     worker_id: int = None, order_id: int = None) -> list[Application]:
    match mode:
        case 'all':
            applications = session.query(Application).all()
        case 'by_customer':
            applications = session.query(Application).filter(Application.customer_id == customer_id).all()
        case 'by worker':
            applications = session.query(Application).filter(Application.freelancer == worker_id).all()
        case 'by_order':
            applications = session.query(Application).filter(Application.order_id == order_id).all()
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    return applications


def get_applications_list_string(
        applications: list, mode: Literal['freelancer', 'customer']
) -> str:
    text = ''
    for application in sorted(applications, key=lambda x: x.id, reverse=True):
        created_at = arrow.get(application.created_at)
        match mode:
            case 'freelancer':
                ...
                # text += (
                #     f"🌐 <b>{order.name}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n"
                #     f"💎 {order.budget}₽ · <i>бюджет проекта</i>\n\n"
                # )
            case 'customer':
                text += f"🌐 id{application.id} · <b>{application.customer_id}</b> · <i>создан {created_at.humanize(locale='ru')}</i>\n\n"
    return text