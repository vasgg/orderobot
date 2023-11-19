from typing import Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_applications_keyboard(
    applications: list, orders: list, mode: Literal['customer', 'freelancer', 'customer_messages', 'freelancer_messages']
) -> InlineKeyboardMarkup:
    orders_dict = {order.id: order for order in orders}
    buttons = []
    for application in sorted(applications, key=lambda x: x.id, reverse=True):
        match mode:
            case 'freelancer':
                fl_buttons = [
                    InlineKeyboardButton(
                        text=f'❌ удалить · id{application.id}',
                        callback_data=f'fl_del_application:{application.id}',
                    ),
                ]
                buttons.append(fl_buttons)
            case 'customer':
                button = [
                    InlineKeyboardButton(
                        text=f'➡️ id{application.id} · {orders_dict[application.order_id].name}',
                        callback_data=f'customer_get_appl_info:{application.id}',
                    )
                ]
                buttons.append(button)
            case 'customer_messages':
                button = [
                    InlineKeyboardButton(
                        text=f'💬 Написать сообщение по заявке · id{application.id}',
                        callback_data=f'customer_send_message:{application.id}',
                    )
                ]
                buttons.append(button)
            case 'freelancer_messages':
                button = [
                    InlineKeyboardButton(
                        text=f'💬 Написать сообщение по заявке · id{application.id}',
                        callback_data=f'fl_send_message:{application.id}',
                    )
                ]
                buttons.append(button)
    buttons.append([InlineKeyboardButton(text='← Закрыть', callback_data='close')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_application_keyboard(application_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💬 Написать сообщение', callback_data=f'fl_send_message:{application_id}'),
            ],
            [
                InlineKeyboardButton(text='✅ Назначить исполнителем', callback_data=f'apply_worker{application_id}'),
            ],
            [
                InlineKeyboardButton(text='← Закрыть', callback_data='close')
            ]
        ]
    )
