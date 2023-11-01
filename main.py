from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import token
from core.resources.middlewares import AuthMiddleware, SessionMiddleware
from core.handlers.common_handlers import router as basic_router
from core.handlers.customer.customer_menu import router as customer_router
from core.handlers.customer.create_order_menu import router as order_menu_router
from core.handlers.freelancer.freelancer_menu import router as freelancer_router
from core.resources.notify_admin import on_shutdown_notify, on_startup_notify


def main():
    bot = Bot(token=token, parse_mode='HTML')
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    dispatcher.message.middleware(SessionMiddleware())
    dispatcher.callback_query.middleware(SessionMiddleware())
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.startup.register(on_startup_notify)
    dispatcher.shutdown.register(on_shutdown_notify)
    dispatcher.include_routers(
        basic_router,
        customer_router,
        freelancer_router,
        order_menu_router,
    )

    dispatcher.run_polling(bot)


if __name__ == '__main__':
    main()
