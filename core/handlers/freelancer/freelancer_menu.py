from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from core.controllers.application_controllers import (
    get_application, get_applications,
    get_applications_list_string, get_projects_list_string, )
from core.controllers.common_controllers import send_message
from core.controllers.order_controllers import (
    get_active_orders, get_order,
    get_orders, get_orders_list_string,
    get_unapplied_orders,
    get_user,
)
from core.controllers.user_controllers import (
    get_deals_counter,
    get_time_since_registration,
)
from core.database.models import User
from core.keyboards.applications_keyboard import get_applications_keyboard, get_project_done_keyboard
from core.keyboards.common_keyboards import (
    account_buttons,
    close_button,
    get_answer_keyboard, get_orders_keyboard,
)
from core.keyboards.freelancer.freelancer_keyboard import (
    get_freelancer_keyboard,
)
from core.resources.dict import answer
from core.resources.enums import OrderStatus, UserType
from core.resources.states import States

router = Router()


@router.callback_query(F.data == "freelancer")
async def freelancer_menu_handler(call: types.CallbackQuery, state: FSMContext, user: User) -> None:
    await state.set_state(States.freelancer_mode)
    await call.message.edit_text(
        text=answer["freelancer_reply"],
        reply_markup=get_freelancer_keyboard(user.balance),
    )
    await state.update_data(current_mode="freelancer")
    await call.answer()


@router.callback_query(F.data == "fl_find_order")
async def fl_find_order_handler(call: types.CallbackQuery, state: FSMContext, user: User, session) -> None:
    orders = await get_orders(user_id=user.id, mode='others', status=OrderStatus.PUBLISHED, session=session)
    applications = await get_applications(session, mode='all')
    filtered_ids = get_unapplied_orders(user.id, orders, applications)
    filtered_orders = [order for order in orders if order.id in filtered_ids]
    text = answer["fl_find_orders_reply"] + get_orders_list_string(filtered_orders, mode="freelancer")
    orders_list = await call.message.answer(
        text=text, reply_markup=get_orders_keyboard(filtered_orders, mode="freelancer")
    )
    await state.update_data(orders_list_message_id=orders_list.message_id)
    await call.answer()


@router.callback_query(F.data.startswith('customer_of_order:'))
async def fl_get_customer_of_order_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split(":")[1])
    order = await get_order(order_id, session)
    customer = await get_user(order.customer_id, session)
    await call.message.answer(
        text=answer["customer_details"].format(
            customer.fullname,
            get_time_since_registration(customer.created_at),
            customer.customer_rating
            if customer.customer_rating
            else "Ещё нет рейтинга",
            await get_deals_counter(customer.id, mode="customer", session=session),
        ),
        reply_markup=close_button,
    ),
    await call.answer()


@router.callback_query(F.data == 'fl_my_projects')
async def fl_my_projects_handler(call: types.CallbackQuery, user: User, session) -> None:
    active_orders = await get_active_orders(mode=UserType.FREELANCER, worker_id=user.id, session=session)
    order_ids = [order.id for order in active_orders]
    projects = []
    for order_id in order_ids:
        application = await get_application(mode='by_order_id', order_id=order_id, session=session)
        projects.append(application)
    text = (answer['fl_projects_reply'] +
            await get_projects_list_string(mode=UserType.FREELANCER, applications=projects, orders=active_orders))
    keyboard = get_applications_keyboard(mode='freelancer_projects', applications=projects, orders=active_orders)
    await call.message.answer_photo(photo=types.FSInputFile(path='core/resources/pictures/projects.jpeg'),
                                    caption=text,
                                    reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data.startswith('fl_mark_as_done:'))
async def fl_mark_as_done_handler(call: types.CallbackQuery, user: User, session) -> None:
    application_id = int(call.data.split(":")[1])
    application = await get_application(mode='by_app_id', application_id=application_id, session=session)
    customer = await get_user(application.customer_id, session=session)
    await call.message.answer(text=answer['fl_done_order_reply'].format(application_id), reply_markup=close_button)
    await send_message(call.message, customer.telegram_id,
                       text=answer['done_order_message_from_freelancer'].format(user.fullname, application_id),
                       reply_markup=get_project_done_keyboard(application_id))
    await call.answer()


@router.callback_query(F.data.in_(['fl_applications', 'fl_messages']))
async def fl_applications_handler(call: types.CallbackQuery, user: User, session) -> None:
    orders = await get_orders(user_id=user.id, mode='others', status=OrderStatus.PUBLISHED, session=session)
    applications = await get_applications(mode='by_worker', worker_id=user.id, session=session)
    text = (answer['fl_applications_reply'] +
            get_applications_list_string(mode=UserType.FREELANCER, applications=applications, orders=orders))
    if call.data == 'fl_applications':
        photo = types.FSInputFile(path='core/resources/pictures/applications.jpeg')
        keyboard = get_applications_keyboard(
            orders=orders, applications=applications, mode="freelancer")
    else:
        photo = types.FSInputFile(path='core/resources/pictures/messages.jpeg')
        keyboard = get_applications_keyboard(
            orders=orders, applications=applications, mode="freelancer_messages")
    await call.message.answer_photo(photo=photo,
                                    caption=text,
                                    reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data.startswith('fl_send_message:'))
async def fl_send_message_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    application_id = int(call.data.split(":")[1])
    msg = await call.message.answer(text=answer['fl_send_message_reply'])
    await state.update_data(fl_message_application_id=application_id,
                            fl_send_message_id=msg.message_id)
    await state.set_state(States.fl_send_message)
    await call.answer()


@router.message(States.fl_send_message)
async def fl_send_message(message: types.Message, state: FSMContext, session) -> None:
    fl_text = message.text
    data = await state.get_data()
    application_id = data.get('fl_message_application_id')
    application = await get_application(mode='by_app_id', application_id=application_id, session=session)
    customer = await get_user(application.customer_id, session)
    freelancer = await get_user(application.freelancer_id, session)
    text = answer['bot_send_message_reply'].format('Фрилансер:', freelancer.fullname, application_id, fl_text)
    await send_message(message, receiver_id=customer.telegram_id, text=text,
                       reply_markup=get_answer_keyboard(mode='freelancer', application_id=application_id))
    await message.delete()
    await message.bot.delete_message(chat_id=message.from_user.id, message_id=data.get('fl_send_message_id'))
    await message.answer(text=answer['bot_message_sent_reply'].format(fl_text, application_id, customer.fullname),
                         reply_markup=close_button)


@router.callback_query(F.data == 'fl_my_account')
async def my_account_handler(call: types.CallbackQuery, user: User, session) -> None:
    time_since_registration = get_time_since_registration(user.created_at)
    rating = user.freelance_rating if user.freelance_rating else 'Ещё нет рейтинга'
    deals = answer['deals_as_freelancer'].format(
        await get_deals_counter(user_id=user.id, mode='freelancer', session=session)
    )
    await call.message.answer_photo(photo=types.FSInputFile(path='core/resources/pictures/account.jpeg'),
                                    caption=answer['my_account_reply'].format(
            user.fullname, time_since_registration, rating, deals, user.balance
        ),
        reply_markup=account_buttons)
    await call.answer()
