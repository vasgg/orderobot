from aiogram import F, Router, types
import arrow

from core.controllers.application_controllers import get_active_application
from core.controllers.order_controllers import get_order, get_user
from core.keyboards.applications_keyboard import get_application_keyboard
from core.resources.dict import answer


router = Router()


@router.callback_query(F.data.startswith('customer_get_appl_info:'))
async def customer_get_application_info_handler(call: types.CallbackQuery, session) -> None:
    application_id = int(call.data.split(':')[1])
    application = await get_active_application(mode='by_app_id', application_id=application_id, session=session)
    created_at = arrow.get(application.created_at)
    order = await get_order(application.order_id, session=session)
    freelancer = await get_user(user_id=application.freelancer_id, session=session)
    await call.message.answer(
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
