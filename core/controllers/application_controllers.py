from typing import Literal

from sqlalchemy.orm import joinedload, selectinload

from core.database.db import db
from core.database.models import Application, Order, User


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
async def create_application(order_id: int, user_id: int, session) -> None:
    new_application = Application(
        order_id=order_id,
        freelancer_id=user_id,
    )
    session.add(new_application)
