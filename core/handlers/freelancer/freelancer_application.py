from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from core.controllers.order_controllers import get_order
from core.keyboards.common_keyboards import get_order_actions_keyboard
from core.keyboards.freelancer.freelancer_keyboard import create_application_buttons
from core.resources.dictionaries import answer
from core.resources.states import States

router = Router()


@router.callback_query(F.data.startswith('fl_get_order_info:'))
async def fl_get_order_info_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = await get_order(order_id, session=session)
    await call.message.answer(
        text=answer["read_order"].format(order.name, order.budget, order.description),
        reply_markup=get_order_actions_keyboard(order.id, mode="freelancer"),
    )
    await call.answer()


@router.callback_query(F.data.startswith('take_order:'))
async def fl_get_order_handler(
    call: types.CallbackQuery, state: FSMContext,
) -> None:
    order_id = int(call.data.split(":")[1])
    await state.update_data(application_draft_order_id=order_id)
    msg = await call.message.edit_text(text=answer['fl_appl_charge_reply'])
    await state.update_data(application_draft_message=msg.message_id)
    await state.set_state(States.fl_appl_charge)
    await call.answer()


@router.message(States.fl_appl_charge)
async def fl_appl_charge_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    try:
        charge = int(message.text)
        data = await state.get_data()
        await state.update_data(application_draft_charge=charge)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['application_draft_message'])
        msg = await message.answer(text=answer['fl_appl_days_reply'])
        await state.update_data(application_draft_message_charge=msg.message_id)
        await state.set_state(States.fl_appl_days)
    except ValueError:
        await message.delete()
        await message.answer(text=answer['incorrect_charge_reply'].format(message.text))


@router.message(States.fl_appl_days)
async def fl_appl_days_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    try:
        days = int(message.text)
        data = await state.get_data()
        await state.update_data(application_draft_days=days)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['application_draft_message_charge'])
        msg = await message.answer(text=answer['fl_appl_message_reply'])
        await state.update_data(application_draft_message_days=msg.message_id)
        await state.set_state(States.fl_appl_message)
    except ValueError:
        await message.delete()
        await message.answer(text=answer['incorrect_days_reply'].format(message.text))


@router.message(States.fl_appl_message)
async def fl_appl_message_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    message_text = message.text
    await state.update_data(application_draft_message=message_text)
    data = await state.get_data()
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['application_draft_message_days'])
    await message.answer(text=answer['fl_appl_final_reply'].format(data['application_draft_charge'],
                                                                   data['application_draft_days'],
                                                                   message_text),
                         reply_markup=create_application_buttons)

