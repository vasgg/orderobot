from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from core.config import settings
from core.controllers.order_controllers import (
    check_order_before_publish,
    delete_draft,
    publish_order_to_db,
    get_customer_draft,
    save_params_to_draft,
    send_order_text_to_channel,
    send_order_text_to_customer,
    validate_url,
)
from core.database.models import User
from core.keyboards.customer.customer_keyboard import get_customer_keyboard
from core.keyboards.customer.new_order_keyboard import (
    back_button,
    change_order_params_keyboard,
    delete_order_keyboad,
    get_publish_order_buttons,
    new_order_buttons,
)
from core.resources.dictionaries import answer
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
                await message.answer(answer['incorrect_url_reply'].format(message.text))


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
        await send_order_text_to_customer(
            call=call,
            order=draft,
            mode='answer',
            state=state,
            markup=get_publish_order_buttons(draft.id),
        )
        # await state.clear()
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
async def forward_order_handler(call: types.CallbackQuery, bot: Bot, session) -> None:
    order_id = int(call.data.split('_')[2])
    await send_order_text_to_channel(bot, order_id, session)
    await call.message.edit_text(
        text=answer['forward_order_reply'].format(settings.CHANNEL_LINK),
        reply_markup=back_button,
    )
    await call.answer()


@router.callback_query(F.data == 'delete_draft')
async def delete_draft_confirm_handler(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    msg = await call.message.answer(
        text=answer['delete_draft_reply'],
        reply_markup=delete_order_keyboad(mode='draft'),
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
