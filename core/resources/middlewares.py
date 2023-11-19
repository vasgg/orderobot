import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import Message
from aiogram.types import TelegramObject, Update

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


class UpdatesDumperMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        json_event = event.model_dump_json(exclude_unset=True)

        res = await handler(event, data)
        if res is UNHANDLED:
            logging.info(json_event)
        return res
