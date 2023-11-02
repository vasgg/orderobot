from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from core.controllers.application_controllers import get_applications
from core.controllers.order_controllers import (
    delete_published_order,
    get_customer_draft,
    get_order,
    get_orders,
    get_orders_list_string,
    send_order_text_to_customer,
)
from core.controllers.user_controllers import get_deals, get_time_since_registration
from core.database.models import User
from core.keyboards.customer.customer_keyboard import get_customer_keyboard
from core.keyboards.customer.new_order_keyboard import (
    delete_order_keyboad,
    new_order_buttons,
)
from core.keyboards.common_keyboards import (
    account_buttons,
    close_button,
    get_order_actions_keyboard,
    get_orders_keyboard,
)
from core.resources.dictionaries import answer
from core.resources.states import States

router = Router()


@router.callback_query(F.data == 'customer')
async def customer_menu_handler(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await state.set_state(States.customer_mode)
    await call.message.edit_text(
        text=answer["customer_reply"], reply_markup=get_customer_keyboard(user.balance)
    )
    await state.update_data(current_mode="customer")
    await call.answer()


@router.callback_query(F.data == 'customer_make_order')
async def customer_make_order_handler(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await state.set_state(States.new_order_draft)
    draft = get_customer_draft(user_id=user.id)
    await send_order_text_to_customer(
        call, draft, mode='edit', state=state, markup=new_order_buttons
    )


@router.callback_query(F.data == 'customer_my_orders')
async def customer_my_orders_handler(call: types.CallbackQuery, user: User, session) -> None:
    orders = get_orders(session, user.id, 'my', status='published')
    text = answer['my_orders_reply'] + get_orders_list_string(orders, mode="customer")
    await call.message.answer(
        text=text, reply_markup=get_orders_keyboard(orders, mode="customer")
    )
    await call.answer()


@router.callback_query(F.data.startswith('customer_get_order_info:'))
async def customer_get_order_info_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = get_order(order_id, session)
    await call.message.edit_text(
        text=answer["read_order"].format(
            order.name, order.budget, order.description, order.link
        ),
        reply_markup=get_order_actions_keyboard(order_id, mode="customer"),
    )
    await call.answer()


@router.callback_query(F.data.startswith('customer_delete_order:'))
async def customer_confirm_deleting_published_order(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    order_id = int(call.data.split(':')[1])
    await state.set_state(States.delete_published_order)
    await call.message.edit_text(
        text=answer["delete_order_reply"],
        reply_markup=delete_order_keyboad(mode='order', order_id=order_id),
    )
    await call.answer()


@router.callback_query(F.data.startswith('delete_published_order:'))
async def customer_delete_published_order(call: types.CallbackQuery) -> None:
    order_id = int(call.data.split(':')[1])
    delete_published_order(order_id)
    await call.message.edit_text(
        text=answer["deleted_order_reply"], reply_markup=close_button
    )


@router.callback_query(F.data == 'customer_applications')
async def customer_applications_handler(
    call: types.CallbackQuery, user: User, session
) -> None:
    applications = get_applications(session, mode='by_customer', customer_id=user.id)


# @router.callback_query(F.data == 'customer_messages')
# async def customer_messages_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...
#
#
# @router.callback_query(F.data == 'customer_drafts')
# async def customer_drafts_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...
#
#
# @router.callback_query(F.data == 'customer_help')
# async def customer_help_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...


@router.callback_query(F.data == 'customer_my_account')
async def customer_my_account_handler(call: types.CallbackQuery, user: User, session) -> None:
    time_since_registration = get_time_since_registration(user.created_at)
    raiting = user.customer_rating if user.customer_rating else 'Ещё нет рейтинга'
    deals = answer["deals_as_customer"].format(
        get_deals(user_id=user.id, mode="customer", session=session)
    )
    await call.message.answer(
        text=answer["my_account_reply"].format(
            user.fullname, time_since_registration, raiting, deals, user.balance
        ),
        reply_markup=account_buttons,
    )
    await call.answer()
