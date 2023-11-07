from typing import Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

new_order_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='✏️ Изменить название', callback_data='change_order_name'
            ),
        ],
        [
            InlineKeyboardButton(
                text='💎 Изменить бюжет', callback_data='change_order_budget'
            ),
        ],
        [
            InlineKeyboardButton(
                text='📄 Изменить описание', callback_data='change_order_description'
            ),
        ],
        [
            InlineKeyboardButton(
                text='🖇️ Добавить ссылку', callback_data='change_order_link'
            ),
        ],
        [
            InlineKeyboardButton(
                text='❌ Удалить черновик', callback_data='delete_draft'
            ),
        ],
        [
            InlineKeyboardButton(text='← Меню заказчика', callback_data='customer'),
            InlineKeyboardButton(text='💠 Опубликовать', callback_data='publish'),
        ],
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='← Назад', callback_data='back_to_order_menu'),
        ]
    ]
)


def get_publish_order_buttons(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='← Назад в меню', callback_data='customer'),
                InlineKeyboardButton(
                    text='⏩ Переслать в канал',
                    callback_data=f'forward_order_{order_id}',
                ),
            ]
        ]
    )


def change_order_params_keyboard(
    mode: Literal['name', 'budget', 'description', 'link']
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💾 Сохранить', callback_data=f'save_order_{mode}'
                ),
                InlineKeyboardButton(
                    text='⌫ Изменить', callback_data=f'change_order_{mode}'
                ),
            ],
        ]
    )

# delete_draft_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text='☑️ Я уверен', callback_data='confirm_delete_draft'
#             ),
#             InlineKeyboardButton(text='❌ Отмена', callback_data='close'),
#         ]
#     ]
# )
