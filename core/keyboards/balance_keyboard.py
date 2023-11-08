from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_back_to_menu_and_pay_buttons(state: FSMContext, amount) -> InlineKeyboardMarkup:
    data = await state.get_data()
    current_mode = data.get('current_mode', 'customer')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='← Главное меню', callback_data=current_mode),
                InlineKeyboardButton(text='💳 Оплатить', callback_data=f'add_funds:{amount * 100}'),
            ]
        ]
    )
