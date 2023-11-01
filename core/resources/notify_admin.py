from aiogram import Bot

from core.config import admin


async def on_startup_notify(bot: Bot):
    await bot.send_message(admin, 'Bot started')


async def on_shutdown_notify(bot: Bot):
    await bot.send_message(admin, 'Bot shutdown')
