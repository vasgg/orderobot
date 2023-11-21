from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from core.config import settings
from core.controllers.application_controllers import get_active_application, get_applications, toggle_application_activeness
from core.controllers.common_controllers import change_order_status, send_message
from core.controllers.order_controllers import (add_worker_to_order, check_balance_before_apply_worker, check_order_before_publish,
                                                delete_draft, get_customer_draft, get_order, get_user, publish_order_to_db,
                                                save_params_to_draft, send_order_text_to_channel, send_order_text_to_customer, validate_url)
from core.controllers.user_controllers import change_user_balance
from core.database.models import User
from core.keyboards.applications_keyboard import get_executior_keyboard
from core.keyboards.common_keyboards import close_button, delete_record_keyboad
from core.keyboards.customer.customer_keyboard import get_customer_keyboard, main_menu_button
from core.keyboards.customer.new_order_keyboard import (
    back_button,
    change_order_params_keyboard,
    get_publish_order_buttons,
    new_order_buttons,
)
from core.resources.dict import answer
from core.resources.enums import OrderStatus, UserType
from core.resources.states import States

router = Router()


@router.callback_query(States.new_order_draft, F.data.startswith('change_order_'))
async def change_order_params_handler(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    action = call.data.split("_")[2]
    match action:
        case 'name':
            await call.message.delete()
            msg = await call.message.answer(
                text=answer['change_order_name_reply'], reply_markup=back_button
            )
            await state.update_data(edit_order_message_id=msg.message_id)
            await state.set_state(States.change_order_name)
        case 'budget':
            await call.message.delete()

            msg = await call.message.answer(
                text=answer['change_order_budget_reply'], reply_markup=back_button
            )
            await state.update_data(edit_order_message_id=msg.message_id)
            await state.set_state(States.change_order_budget)
        case 'description':
            await call.message.delete()

            msg = await call.message.answer(
                text=answer['change_order_description_reply'], reply_markup=back_button
            )
            await state.update_data(edit_order_message_id=msg.message_id)
            await state.set_state(States.change_order_description)
        case 'link':
            await call.message.delete()

            msg = await call.message.answer(
                text=answer['change_order_link_reply'], reply_markup=back_button
            )
            await state.update_data(edit_order_message_id=msg.message_id)
            await state.set_state(States.change_order_link)
    await call.answer()


@router.message(States.change_order_name)
@router.message(States.change_order_budget)
@router.message(States.change_order_description)
@router.message(States.change_order_link)
async def check_order_params_handler(
    message: types.Message, state: FSMContext, user: User, session
) -> None:
    current_state = await state.get_state()
    draft = await get_customer_draft(user_id=user.id, session=session)
    match current_state:
        case 'States:change_order_name':
            await message.delete()
            new_name = message.text
            await save_params_to_draft(order_id=draft.id, mode='name', value=new_name, session=session)
            await message.answer(
                answer['check_param_reply'].format('Введено имя заказа', new_name),
                reply_markup=change_order_params_keyboard('name'),
            )
            await state.set_state(States.new_order_draft)
        case 'States:change_order_budget':
            await message.delete()
            new_budget = message.text
            await save_params_to_draft(order_id=draft.id, mode='budget', value=new_budget, session=session)
            await message.answer(
                answer['check_balance_reply'].format(
                    'Введён бюджет заказа', new_budget
                ),
                reply_markup=change_order_params_keyboard('budget'),
            )
            await state.set_state(States.new_order_draft)
        case 'States:change_order_description':
            await message.delete()
            new_description = message.text
            await save_params_to_draft(
                order_id=draft.id, mode='description', value=new_description, session=session
            )
            await message.answer(
                answer['check_param_reply'].format(
                    'Введено описание заказа', new_description
                ),
                reply_markup=change_order_params_keyboard('description'),
            )
            await state.set_state(States.new_order_draft)
        case 'States:change_order_link':
            await message.delete()
            new_link = message.text
            if validate_url(new_link):
                await save_params_to_draft(order_id=draft.id, mode='link', value=new_link, session=session)
                msg = await message.answer(
                    answer['check_param_reply'].format('Введён URL-адрес', new_link),
                    reply_markup=change_order_params_keyboard('link'),
                )
                await state.update_data(edit_order_confirm_id=msg.message_id)
                await state.set_state(States.new_order_draft)
            else:
                await message.answer(answer['incorrect_url_reply'].format(message.text), reply_markup=back_button)


@router.callback_query(F.data == 'back_to_order_menu')
async def back_to_order_handler(
    call: types.CallbackQuery, state: FSMContext, user: User
) -> None:
    await call.message.edit_text(
        text=answer['customer_reply'], reply_markup=get_customer_keyboard(user.balance)
    )
    await state.set_state(States.new_order_draft)
    await call.answer()


@router.callback_query(States.change_order_name)
@router.callback_query(States.change_order_budget)
@router.callback_query(States.change_order_description)
@router.callback_query(States.change_order_link)
@router.callback_query(F.data.startswith('save_order_'))
async def save_order_params_handler(
    call: types.CallbackQuery, state: FSMContext, user: User, bot: Bot, session
) -> None:
    action = call.data.split("_")[2]
    draft = await get_customer_draft(user_id=user.id, session=session)
    data = await state.get_data()
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=data['edit_order_message_id']
    )
    match action:
        case 'name':
            await send_order_text_to_customer(
                call=call,
                order=draft,
                mode='edit',
                state=state,
                markup=new_order_buttons,
            )
        case 'budget':
            await send_order_text_to_customer(
                call=call,
                order=draft,
                mode='edit',
                state=state,
                markup=new_order_buttons,
            )
        case 'description':
            await send_order_text_to_customer(
                call=call,
                order=draft,
                mode='edit',
                state=state,
                markup=new_order_buttons,
            )
        case 'link':
            await send_order_text_to_customer(
                call=call,
                order=draft,
                mode='edit',
                state=state,
                markup=new_order_buttons,
            )
    await call.answer()


@router.callback_query(F.data == 'publish')
async def publish_order_handler(
    call: types.CallbackQuery, state: FSMContext, user: User, session
) -> None:
    draft = await get_customer_draft(user_id=user.id, session=session)
    condition = check_order_before_publish(draft)
    if isinstance(condition, bool):
        await publish_order_to_db(draft, user, session)
        text = answer["publish_order_reply"] + answer["post_order"].format(
            draft.id, draft.name, draft.budget, draft.link, draft.description)
        msg = await call.message.edit_text(text=text, reply_markup=get_publish_order_buttons(draft.id))
        await state.update_data(published_message_id=msg.message_id)
    else:
        missing_conditions = []
        for field, value in condition._asdict().items():
            if not value:
                missing_conditions.append(field)
        await call.message.edit_text(
            text=answer['publish_order_error_reply'].format(
                ', '.join(missing_conditions)
            ),
            reply_markup=new_order_buttons,
        )
    await call.answer()


@router.callback_query(F.data.startswith('forward_order_'))
async def forward_order_handler(call: types.CallbackQuery, session) -> None:
    order_id = int(call.data.split('_')[2])
    await send_order_text_to_channel(call, order_id, session)
    await call.message.edit_text(
        text=answer['forward_order_reply'].format(settings.CHANNEL_LINK),
        reply_markup=main_menu_button,
    )
    await call.answer()


@router.callback_query(F.data == 'delete_draft')
async def delete_draft_confirm_handler(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    msg = await call.message.answer(
        text=answer['delete_draft_reply'],
        reply_markup=delete_record_keyboad(mode='draft'),
    )
    await state.update_data(delete_order_message_id=msg.message_id)
    await call.answer()


@router.callback_query(F.data == 'confirm_delete_draft')
async def delete_draft_handler(call: types.CallbackQuery, user: User, session) -> None:
    await delete_draft(user.id, session)
    await call.message.edit_text(
        text=answer['customer_reply'], reply_markup=get_customer_keyboard(user.balance)
    )
    await call.answer()


@router.callback_query(F.data.startswith('apply_worker:'))
async def apply_worker_handler(call: types.CallbackQuery, user: User, session) -> None:
    application_id = int(call.data.split(':')[1])
    application = await get_active_application(mode='by_app_id', application_id=application_id, session=session)
    customer = await get_user(user_id=application.customer_id, session=session)
    order = await get_order(application.order_id, session=session)
    freelancer = application.freelancer
    if not check_balance_before_apply_worker(application_fee=application.fee, user_balance=user.balance):
        await call.message.answer(text=answer['insufficient_funds_reply'], reply_markup=close_button)
        return
    await change_user_balance(telegram_id=call.from_user.id, current_balance=user.balance, amount=application.fee,
                              mode='subtract', session=session)
    await change_order_status(entity=application.order, entity_id=application.order_id, status=OrderStatus.WIP, session=session)
    await add_worker_to_order(order_id=application.order_id, worker_id=application.freelancer_id, session=session)
    applications = await get_applications(order_id=application.order_id, mode='by_order', session=session)
    for application in applications:
        await toggle_application_activeness(application.id, session=session)
    text_to_executor = answer['apply_worker_reply_to_fl'].format(customer.fullname, application.order_id, application.id, order.name,
                                                                 order.description, application.fee, application.completion_days)
    await send_message(message=call.message, receiver_id=freelancer.telegram_id,
                       text=text_to_executor, reply_markup=get_executior_keyboard(application_id, mode=UserType.FREELANCER))
    await call.message.edit_text(text=answer['apply_worker_reply_to_customer'],
                                 reply_markup=get_executior_keyboard(application_id, mode=UserType.CUSTOMER))
    await call.answer()
