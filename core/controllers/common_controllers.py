from aiogram import types
from sqlalchemy import update

from core.database.models import Application, Order
from core.resources.enums import OrderStatus


async def change_order_status(entity: [Order, Application], entity_id: int, status: OrderStatus, session) -> None:
    query = update(entity.__table__).filter_by(id=entity_id).values(status=status)
    await session.execute(query)


async def send_message(message: types.Message, receiver_id: int, text: str, reply_markup: types.InlineKeyboardMarkup) -> None:
    await message.bot.send_message(chat_id=receiver_id,
                                   text=text,
                                   reply_markup=reply_markup)
