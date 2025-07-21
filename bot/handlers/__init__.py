from aiogram import Router, Dispatcher

from . import start, registration, admin

def setup_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(admin.router)