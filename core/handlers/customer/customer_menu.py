from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from core.controllers.application_controllers import (
    get_application, get_applications,
    get_applications_list_string, send_message,
)
from core.controllers.order_controllers import (
    delete_published_order,
    get_customer_draft,
    get_order,
    get_orders,
    get_orders_list_string,
    get_user, send_order_text_to_customer,
)
from core.controllers.user_controllers import (
    get_deals_counter,
    get_time_since_registration,
)
from core.database.models import User
from core.keyboards.common_keyboards import (
    account_buttons,
    close_button,
    delete_record_keyboad,
    get_answer_keyboard, get_order_actions_keyboard,
    get_orders_keyboard,
)
from core.keyboards.customer.customer_keyboard import get_customer_keyboard
from core.keyboards.customer.new_order_keyboard import (
    new_order_buttons,
)
from core.keyboards.freelancer.applications_keyboard import get_applications_keyboard
from core.resources.dict import answer
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
    call: types.CallbackQuery, state: FSMContext, user: User, session
) -> None:
    await state.set_state(States.new_order_draft)
    draft = await get_customer_draft(user_id=user.id, session=session)
    await send_order_text_to_customer(
        call, draft, mode='edit', state=state, markup=new_order_buttons
    )


@router.callback_query(F.data == 'customer_my_orders')
async def customer_my_orders_handler(
    call: types.CallbackQuery, user: User, session
) -> None:
    orders = await get_orders(session, user.id, 'my', status='published')
    text = answer['my_orders_reply'] + get_orders_list_string(orders, mode="customer")
    await call.message.answer_photo(
        photo=types.FSInputFile(path='core/resources/pictures/orders.jpeg'),
        caption=text,
        reply_markup=get_orders_keyboard(orders, mode="customer"),
    )
    await call.answer()


@router.callback_query(F.data.startswith('customer_get_order_info:'))
async def customer_get_order_info_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = await get_order(order_id, session)
    await call.message.answer(
        text=answer["read_order"].format(
            order.name, order.budget, order.description, order.link
        ),
        reply_markup=get_order_actions_keyboard(order_id, mode="customer"),
    )
    await call.answer()


@router.callback_query(F.data.startswith('customer_delete_order:'))
async def customer_confirm_deleting_published_order(call: types.CallbackQuery) -> None:
    order_id = int(call.data.split(':')[1])
    await call.message.edit_text(
        text=answer["delete_order_reply"],
        reply_markup=delete_record_keyboad(mode='order', record_id=order_id),
    )
    await call.answer()


@router.callback_query(F.data.startswith('delete_published_order:'))
async def customer_delete_published_order(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(':')[1])
    await delete_published_order(order_id, session)
    await call.message.edit_text(
        text=answer["deleted_order_reply"], reply_markup=close_button
    )
    await call.answer()


@router.callback_query(F.data.in_(['customer_applications', 'customer_messages']))
async def customer_applications_handler(
    call: types.CallbackQuery, user: User, session
) -> None:
    orders = await get_orders(mode='my', user_id=user.id, status='published', session=session)
    applications = await get_applications(session, mode='by_customer', customer_id=user.id)
    text = answer['customer_applications_reply'] + get_applications_list_string(
        applications=applications, orders=orders, mode="customer")
    if call.data == 'customer_applications':
        photo = types.FSInputFile(path='core/resources/pictures/applications.jpeg')
        keyboard = get_applications_keyboard(
            orders=orders, applications=applications, mode="customer")
    else:
        photo = types.FSInputFile(path='core/resources/pictures/messages.jpeg')
        keyboard = get_applications_keyboard(
            orders=orders, applications=applications, mode="customer_messages")
    await call.message.answer_photo(photo=photo,
                                    caption=text,
                                    reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data.startswith('customer_send_message:'))
async def customer_send_message_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    application_id = int(call.data.split(":")[1])
    msg = await call.message.answer(text=answer['customer_send_message_reply'])
    await state.update_data(customer_message_application_id=application_id,
                            customer_send_message_id=msg.message_id)
    await state.set_state(States.customer_send_message)
    await call.answer()


@router.message(States.customer_send_message)
async def customer_send_message(message: types.Message, state: FSMContext, session) -> None:
    customer_text = message.text
    data = await state.get_data()
    application_id = data.get('customer_message_application_id')
    application = await get_application(application_id, session)
    customer = await get_user(application.customer_id, session)
    freelancer = await get_user(application.freelancer_id, session)
    text = answer['bot_send_message_reply'].format('Заказчик:', customer.fullname, application_id, customer_text)
    await send_message(message, receiver_id=freelancer.telegram_id, text=text,
                       reply_markup=get_answer_keyboard(mode='customer', application_id=application_id))
    await message.delete()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=data.get('customer_send_message_id'))
    await message.answer(text=answer['bot_message_sent_reply'].format(customer_text, application_id, freelancer.fullname),
                         reply_markup=close_button)


@router.callback_query(F.data == 'customer_my_account')
async def customer_my_account_handler(
    call: types.CallbackQuery, user: User, session
) -> None:
    time_since_registration = get_time_since_registration(user.created_at)
    raiting = user.customer_rating if user.customer_rating else 'Ещё нет рейтинга'
    deals = answer["deals_as_customer"].format(
        await get_deals_counter(user_id=user.id, mode="customer", session=session)
    )
    format_text = answer["my_account_reply"].format(
        user.fullname, time_since_registration, raiting, deals, user.balance
    )
    await call.message.answer_photo(
        photo=types.FSInputFile(path='core/resources/pictures/account.jpeg'),
        caption=format_text,
        reply_markup=account_buttons,
    )
    await call.answer()
