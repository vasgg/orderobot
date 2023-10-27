from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_back_to_menu_button(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    current_mode = data.get('current_mode', 'customer')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='← Главное меню', callback_data=current_mode),
            ]
        ]
    )


async def get_back_to_menu_and_pay_buttons(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    current_mode = data.get('current_mode', 'customer')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='← Главное меню', callback_data=current_mode),
                InlineKeyboardButton(text='💳 Оплатить', callback_data='add_funds')
            ]
        ]
    )
