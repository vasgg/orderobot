from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from core.controllers.user_controllers import get_user_from_db
from core.database.db import db


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with db.session_factory.begin() as session:
            data['session'] = session
            res = await handler(event, data)
            await session.commit()
            return res


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session = data['session']
        user = await get_user_from_db(event, session)
        data['user'] = user

        return await handler(event, data)


