from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_customer_keyboard(balance: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⚡️ Создать заказ', callback_data='customer_make_order'),
                InlineKeyboardButton(text='🔼 Заявки', callback_data='customer_applications'),
            ],
            [
                InlineKeyboardButton(text='🗂️ Мои заказы', callback_data='customer_my_orders'),
                InlineKeyboardButton(text='💬 Сообщения', callback_data='customer_messages'),
            ],
            [
                InlineKeyboardButton(text='ℹ️ Инструкция', callback_data='information'),
                InlineKeyboardButton(text=f'💎 {balance}₽', callback_data='user_balance'),
            ],
            [
                InlineKeyboardButton(text='👾 Мой аккаунт', callback_data='customer_my_account'),
            ],
            [
                InlineKeyboardButton(text='🔁 Режим фрилансера', callback_data='freelancer'),
            ]
        ],
    )


application_receive_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='← Закрыть', callback_data='close'),
            InlineKeyboardButton(text='🔼 Заявки', callback_data='customer_applications'),
        ]
    ]
)
