from typing import Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.resources.enums import UserType


def get_applications_keyboard(
    applications: list, orders: list, mode:
        Literal['freelancer', 'customer', 'freelancer_messages', 'customer_messages', 'freelancer_projects', 'customer_projects']
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
            case 'freelancer_messages':
                button = [
                    InlineKeyboardButton(
                        text=f'💬 Написать сообщение по заявке · id{application.id}',
                        callback_data=f'fl_send_message:{application.id}',
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
            case 'freelancer_projects':
                keys = (
                    [
                        InlineKeyboardButton(
                            text=f'💬 Написать сообщение по заявке · id{application.id}',
                            callback_data=f'fl_send_message:{application.id}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=f'✅ Отметить выполненным · id{application.id}',
                            callback_data=f'fl_mark_as_done:{application.id}',
                        )
                    ]
                )
                buttons.extend(keys)
            case 'customer_projects':
                keys = [
                    [
                        InlineKeyboardButton(
                            text=f'💬 Написать сообщение по заявке · id{application.id}',
                            callback_data=f'customer_send_message:{application.id}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=f'✅ Отметить выполненным · id{application.id}',
                            callback_data=f'customer_mark_as_done:{application.id}',
                        )
                    ]
                ]
                buttons.extend(keys)
    buttons.append([InlineKeyboardButton(text='← Закрыть', callback_data='close')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_application_keyboard(application_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💬 Написать сообщение', callback_data=f'customer_send_message:{application_id}'),
            ],
            [
                InlineKeyboardButton(text='✅ Назначить исполнителем', callback_data=f'apply_worker:{application_id}'),
            ],
            [
                InlineKeyboardButton(text='← Закрыть', callback_data='close')
            ]
        ]
    )


def get_executior_keyboard(application_id: int, mode: UserType) -> InlineKeyboardMarkup:
    match mode:
        case UserType.FREELANCER:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='💬 Написать сообщение', callback_data=f'fl_send_message:{application_id}'),
                    ],
                    [
                        InlineKeyboardButton(text='← Закрыть', callback_data='close')
                    ]
                ]
            )
        case UserType.CUSTOMER:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='💬 Написать сообщение', callback_data=f'customer_send_message:{application_id}'),
                    ],
                    [
                        InlineKeyboardButton(text='← Закрыть', callback_data='close')
                    ]
                ]
            )


def get_project_done_keyboard(application_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f'💬 Написать сообщение по заявке · id{application_id}',
                            callback_data=f'customer_send_message:{application_id}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text='← Закрыть',
                            callback_data='close',
                        ),
                        InlineKeyboardButton(
                            text=f'✅ Выполнено · id{application_id}',
                            callback_data=f'customer_mark_as_done:{application_id}',
                        ),
                    ],
        ]
    )
