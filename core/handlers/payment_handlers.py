from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from core.config import settings
from core.controllers.user_controllers import change_user_balance
from core.database.models import User
from core.keyboards.common_keyboards import role_selector
from core.keyboards.customer.customer_keyboard import get_customer_keyboard
from core.keyboards.freelancer.freelancer_keyboard import get_freelancer_keyboard
from core.resources.dict import answer

router = Router()


@router.callback_query(F.data.startswith('add_funds:'))
async def begin_process_payment(call: types.CallbackQuery, state: FSMContext) -> None:
    amount = int(call.data.split(":")[1])
    await state.update_data(added_funds_amount=amount / 100)
    price = types.LabeledPrice(label='Пополнение баланса бота', amount=amount)
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Пополнение баланса бота',
        description='Начисление на ваш баланс в боте указанной суммы в рублях',
        payload='test payment from Youkassa',
        provider_token=settings.PAYMASER_TOKEN.get_secret_value(),
        currency='RUB',
        prices=[price],
    )
    await call.answer()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def finish_payment(message: types.Message, state: FSMContext, user: User, session) -> None:
    data = await state.get_data()
    await change_user_balance(telegram_id=message.from_user.id,
                              current_balance=user.balance,
                              amount=data['added_funds_amount'],
                              mode='add',
                              session=session)
    try:
        match data['current_mode']:
            case 'freelancer':
                await message.answer(text=answer["freelancer_reply"], reply_markup=get_freelancer_keyboard(user.balance))
            case 'customer':
                await message.answer(text=answer["customer_reply"], reply_markup=get_customer_keyboard(user.balance))
    except KeyError:
        await message.answer(text=answer["start_reply"], reply_markup=role_selector)
