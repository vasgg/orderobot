from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from core.controllers.order_controllers import (
    get_user,
    get_order,
    get_orders,
    get_orders_list_string,
)
from core.controllers.application_controllers import create_application
from core.controllers.user_controllers import get_deals, get_time_since_registration
from core.database.models import User
from core.keyboards.freelancer.freelancer_keyboard import (
    get_freelancer_keyboard,
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


@router.callback_query(F.data == "freelancer")
async def freelancer_menu_handler(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await state.set_state(States.freelancer_mode)
    await call.message.edit_text(
        text=answer["freelancer_reply"],
        reply_markup=get_freelancer_keyboard(user.balance),
    )
    await state.update_data(current_mode="freelancer")
    await call.answer()


@router.callback_query(F.data == "fl_find_order")
async def fl_find_order_handler(
    call: types.CallbackQuery, state: FSMContext, user: User, session
) -> None:
    orders = get_orders(user_id=user.id, mode="others", status="published", session=session)
    text = answer["fl_find_orders_reply"] + get_orders_list_string(
        orders, mode="freelancer"
    )
    orders_list = await call.message.answer(
        text=text, reply_markup=get_orders_keyboard(orders, mode="freelancer")
    )
    await state.update_data(orders_list_message_id=orders_list.message_id)
    await call.answer()


@router.callback_query(F.data.startswith('fl_get_order_info:'))
async def fl_get_order_info_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = get_order(order_id, session=session)
    await call.message.edit_text(
        text=answer["read_order"].format(order.name, order.budget, order.description),
        reply_markup=get_order_actions_keyboard(order.id, mode="freelancer"),
    )
    await call.answer()


@router.callback_query(F.data.startswith('take_order:'))
async def fl_get_order_handler(call: types.CallbackQuery, user: User, session, bot: Bot) -> None:
    order_id = int(call.data.split(":")[1])
    order = get_order(order_id, session=session)
    await create_application(order_id=order_id, user_id=user.id, session=session)
    await call.message.edit_text(
        text=answer["fl_take_order_reply"].format(order.name),
        reply_markup=close_button
        # reply_markup=get_order_actions_keyboard(order.id, mode="freelancer"),
    )
    user = get_user(user_id=order.customer_id, session=session)
    await bot.send_message(chat_id=user.telegram_id, text=answer["fl_take_order_from_customer"])
    await call.answer()


@router.callback_query(F.data.startswith('customer_of_order:'))
async def fl_get_customer_of_order_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = get_order(order_id, session)
    customer = get_user(order.customer_id, session)
    await call.message.answer(
        text=answer["customer_details"].format(
            customer.fullname,
            get_time_since_registration(customer.created_at),
            customer.customer_rating
            if customer.customer_rating
            else "Ещё нет рейтинга",
            get_deals(customer.id, mode="customer", session=session),
        ),
        reply_markup=close_button,
    ),
    await call.answer()


# @router.callback_query(F.data == "fl_my_projects")
# async def fl_my_projects_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...


@router.callback_query(F.data == "fl_applications")
async def fl_applications_handler(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    ...


# @router.callback_query(F.data == "fl_messages")
# async def fl_messages_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...
#
#
# @router.callback_query(F.data == "fl_help")
# async def fl_help_handler(
#     call: types.CallbackQuery, state: FSMContext, bot: Bot
# ) -> None:
#     ...

# @router.callback_query(F.data.startswith("fl_get_order_info"))
# async def read_order_info(call: types.CallbackQuery, state: FSMContext) -> None:
#     order_number = int(call.data.split(":")[1])
#     order_text = get_order_info(call.from_user.id, order_number)
#     orders_list = await call.message.answer(
#         text=order_text, reply_markup=get_order_info_buttons(oder_number=order_number)
#     )
#     await state.update_data(orders_list_message_id=orders_list.message_id)
#     await call.answer()


@router.callback_query(F.data == "fl_my_account")
async def my_account_handler(call: types.CallbackQuery, user: User, session) -> None:
    time_since_registration = get_time_since_registration(user.created_at)
    raiting = user.freelance_rating if user.freelance_rating else "Ещё нет рейтинга"
    deals = answer["deals_as_freelancer"].format(
        get_deals(user_id=user.id, mode="freelancer", session=session)
    )
    await call.message.answer(
        text=answer["my_account_reply"].format(
            user.fullname, time_since_registration, raiting, deals, user.balance
        ),
        reply_markup=account_buttons,
    )
    await call.answer()
