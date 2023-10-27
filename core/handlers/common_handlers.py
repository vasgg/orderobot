from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from core.controllers.user_controllers import rename_user
from core.database.models import User
from core.keyboards.common_keyboards import close_button, role_selector
from core.resources.dictionaries import answer
from core.resources.states import States

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext) -> None:
    msg = await message.answer(
        text=answer["start_reply"],
        reply_markup=role_selector,
    )
    await state.update_data(main_menu_message_id=msg.message_id)


@router.callback_query(F.data == 'close')
async def close_message(call: types.CallbackQuery) -> None:
    await call.message.delete()
    await call.answer()


@router.callback_query(F.data == 'rename_account')
async def rename_account_handler(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await state.set_state(States.rename_account)
    msg = await call.message.answer(
        text=answer['rename_account_reply'].format(user.fullname)
    )
    await state.update_data(rename_account_message_id=msg.message_id)
    await call.answer()


@router.message(States.rename_account)
async def rename_account(message: types.Message, state: FSMContext, bot: Bot) -> None:
    new_name = message.text
    rename_user(message.from_user.id, new_name)
    await message.answer(
        text=answer['rename_account_success'].format(new_name),
        reply_markup=close_button,
    )
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=data['rename_account_message_id']
    )
