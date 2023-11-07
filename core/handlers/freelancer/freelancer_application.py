from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
import arrow

from core.controllers.application_controllers import (
    create_application,
    del_application,
    get_application,
)
from core.controllers.order_controllers import get_order, get_user
from core.database.models import User
from core.keyboards.common_keyboards import (
    close_button,
    delete_record_keyboad,
    get_order_actions_keyboard,
)
from core.keyboards.customer.customer_keyboard import application_receive_buttons
from core.keyboards.freelancer.applications_keyboard import get_application_keyboard
from core.keyboards.freelancer.freelancer_keyboard import (
    application_send_buttons,
    get_application_buttons,
)
from core.resources.dict import answer
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
    call: types.CallbackQuery,
    state: FSMContext,
) -> None:
    order_id = int(call.data.split(":")[1])
    await state.update_data(application_draft_order_id=order_id)
    msg = await call.message.edit_text(text=answer['fl_appl_charge_reply'])
    await state.update_data(application_draft_message=msg.message_id)
    await state.set_state(States.fl_appl_charge)
    await call.answer()


@router.message(States.fl_appl_charge)
async def fl_appl_charge_handler(
    message: types.Message, state: FSMContext, bot: Bot
) -> None:
    try:
        charge = int(message.text)
        data = await state.get_data()
        await state.update_data(application_draft_charge=charge)
        await message.delete()
        await bot.delete_message(
            chat_id=message.from_user.id, message_id=data['application_draft_message']
        )
        msg = await message.answer(text=answer['fl_appl_days_reply'])
        await state.update_data(application_draft_message_charge=msg.message_id)
        await state.set_state(States.fl_appl_days)
    except ValueError:
        await message.answer(text=answer['incorrect_charge_reply'].format(message.text))


@router.message(States.fl_appl_days)
async def fl_appl_days_handler(
    message: types.Message, state: FSMContext, bot: Bot
) -> None:
    try:
        days = int(message.text)
        data = await state.get_data()
        await state.update_data(application_draft_days=days)
        await message.delete()
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=data['application_draft_message_charge'],
        )
        msg = await message.answer(text=answer['fl_appl_message_reply'])
        await state.update_data(application_draft_message_days=msg.message_id)
        await state.set_state(States.fl_appl_message)
    except ValueError:
        await message.answer(text=answer['incorrect_days_reply'].format(message.text))


@router.message(States.fl_appl_message)
async def fl_appl_message_handler(
    message: types.Message, state: FSMContext, bot: Bot
) -> None:
    message_text = message.text
    await state.update_data(application_draft_message=message_text)
    data = await state.get_data()
    await message.delete()
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=data['application_draft_message_days']
    )
    await message.answer(
        text=answer['fl_appl_final_reply'].format(
            data['application_draft_charge'],
            data['application_draft_days'],
            message_text,
        ),
        reply_markup=get_application_buttons(data['application_draft_order_id']),
    )


@router.callback_query(F.data.startswith('fl_send_application:'))
async def fl_send_application_handler(
    call: types.CallbackQuery, state: FSMContext, user: User, bot: Bot, session
) -> None:
    order_id = int(call.data.split(":")[1])
    order = await get_order(order_id, session=session)
    data = await state.get_data()
    await create_application(
        order_id=order_id,
        customer_id=order.customer_id,
        freelancer_id=user.id,
        fee=data['application_draft_charge'],
        completion_days=data['application_draft_days'],
        message=data['application_draft_message'],
        session=session,
    )
    await call.message.edit_text(
        text=answer["fl_take_order_reply"].format(order.name),
        # reply_markup=close_button
        reply_markup=application_send_buttons,
    )
    customer = await get_user(user_id=order.customer_id, session=session)
    await bot.send_message(
        chat_id=customer.telegram_id,
        text=answer["fl_take_order_from_customer"].format(order.name),
        reply_markup=application_receive_buttons,
    )
    await call.answer()


@router.callback_query(F.data.startswith('fl_del_application:'))
async def fl_delete_application_dialog(
    call: types.CallbackQuery,
) -> None:
    application_id = int(call.data.split(":")[1])
    await call.message.answer(
        text=answer["delete_application_reply"],
        reply_markup=delete_record_keyboad(
            mode='application', record_id=application_id
        ),
    )
    await call.answer()


@router.callback_query(F.data.startswith('delete_application:'))
async def customer_delete_application_handler(
    call: types.CallbackQuery, session
) -> None:
    application_id = int(call.data.split(':')[1])
    await del_application(application_id, session=session)
    await call.message.edit_text(
        text=answer["deleted_application_reply"], reply_markup=close_button
    )
    await call.answer()


@router.callback_query(F.data.startswith('customer_get_appl_info:'))
async def customer_get_application_info_handler(
    call: types.CallbackQuery, session
) -> None:
    application_id = int(call.data.split(':')[1])
    application = await get_application(application_id, session=session)
    created_at = arrow.get(application.created_at)
    order = await get_order(application.order_id, session=session)
    freelancer = await get_user(user_id=application.freelancer_id, session=session)
    await call.message.edit_text(
        text=answer["application_reply"].format(
            order.name,
            application_id,
            freelancer.fullname,
            created_at.humanize(locale='ru'),
            application.fee,
            application.completion_days,
            application.message
        ),
        reply_markup=get_application_keyboard(application_id),
    )
    await call.answer()
