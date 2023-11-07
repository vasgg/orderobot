from typing import Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_orders_keyboard(
    orders: list, mode: Literal['customer', 'freelancer']
) -> InlineKeyboardMarkup:
    buttons = []
    for order in sorted(orders, key=lambda x: x.id, reverse=True):
        match mode:
            case 'customer':
                button = [
                    InlineKeyboardButton(
                        text=f'➡️ id{order.id} · {order.name}',
                        callback_data=f'customer_get_order_info:{order.id}',
                    )
                ]
                buttons.append(button)
            case 'freelancer':
                button = [
                    InlineKeyboardButton(
                        text=f'➡️ id{order.id} · {order.name}',
                        callback_data=f'fl_get_order_info:{order.id}',
                    )
                ]
                buttons.append(button)
    buttons.append([InlineKeyboardButton(text='← Закрыть', callback_data='close')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_order_actions_keyboard(
    order_id: int, mode: Literal['customer', 'freelancer']
) -> InlineKeyboardMarkup:
    buttons = []
    match mode:
        case 'customer':
            buttons.append(
                [
                    InlineKeyboardButton(
                        text='🗑 Удалить заказ',
                        callback_data=f'customer_delete_order:{order_id}',
                    )
                ]
            )
        case 'freelancer':
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text='💼 Заказчик',
                            callback_data=f'customer_of_order:{order_id}',
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text='⚡️ Взять заказ',
                            callback_data=f'take_order:{order_id}',
                        )
                    ],
                ]
            )
    buttons.append([InlineKeyboardButton(text='← Закрыть', callback_data='close')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


role_selector = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💼 Режим заказчика', callback_data='customer'),
        ],
        [
            InlineKeyboardButton(
                text='‍💻 Режим фрилансера', callback_data='freelancer'
            ),
        ],
    ],
)


close_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='← Закрыть', callback_data='close'),
        ]
    ]
)


account_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💳 Пополнить баланс', callback_data='user_balance'
                ),
                InlineKeyboardButton(text='💵 Вывод средств', callback_data='withdraw'),
            ],
            [
                InlineKeyboardButton(
                    text='📝 Изменить публичное имя', callback_data='rename_account'
                ),
            ],
            [
                InlineKeyboardButton(text='← Закрыть', callback_data='close'),
            ],
        ]
    )


def delete_record_keyboad(
    mode: Literal['draft', 'order', 'application'], record_id: int = None
) -> InlineKeyboardMarkup:
    buttons = []
    match mode:
        case 'draft':
            buttons.append(
                [
                    InlineKeyboardButton(text='⌫ Отмена', callback_data='сlose'),
                    InlineKeyboardButton(
                        text='❌ Удалить', callback_data='confirm_delete_draft'
                    ),
                ]
            )
        case 'order':
            buttons.append(
                [
                    InlineKeyboardButton(text='⌫ Отмена', callback_data='close'),
                    InlineKeyboardButton(
                        text='❌ Удалить',
                        callback_data=f'delete_published_order:{record_id}',
                    ),
                ]
            )
        case 'application':
            buttons.append(
                [
                    InlineKeyboardButton(text='⌫ Отмена', callback_data='close'),
                    InlineKeyboardButton(
                        text='❌ Удалить',
                        callback_data=f'delete_application:{record_id}'
                    )
                ]
            )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
