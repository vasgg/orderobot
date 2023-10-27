from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_freelancer_keyboard(balance: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔎 Найти заказ', callback_data='fl_find_order'),
                InlineKeyboardButton(text='🔼 Заявки', callback_data='fl_applications'),
            ],
            [
                InlineKeyboardButton(text='🗂️ Проекты', callback_data='fl_my_projects'),
                InlineKeyboardButton(text='💬 Сообщения', callback_data='fl_messages'),
            ],
            [
                InlineKeyboardButton(text='ℹ️ Инструкция', callback_data='fl_help'),
                InlineKeyboardButton(text=f'💎 {balance} ₽', callback_data='user_balance'),
            ],
            [
                InlineKeyboardButton(text='👾 Мой аккаунт', callback_data='fl_my_account'),
            ],
            [
                InlineKeyboardButton(text='🔁 Режим заказчика', callback_data='customer'),
            ]
        ],
    )
