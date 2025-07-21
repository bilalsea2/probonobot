import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards import language_kb
from bot.localization import get_text
from bot.utils import check_channel_subscription, is_user_registered
from bot.states.registration import RegistrationStates
from config import CHANNEL_ID

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Please choose your language:\nIltimos, tilingizni tanlang:", reply_markup=language_kb())

@router.callback_query(F.data.in_({'lang_uz', 'lang_en'}))
async def select_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split('_')[1]
    await state.update_data(lang=lang)
    await callback.message.edit_text(get_text(lang, 'language_selected'))

    is_subscribed = await check_channel_subscription(callback.bot, callback.from_user.id, CHANNEL_ID)

    if not is_subscribed:
        await callback.message.answer(get_text(lang, 'not_subscribed').format(channel_link=f"https://t.me/c/{str(CHANNEL_ID)[4:]}"))
        await state.clear()
        return

    if is_user_registered(callback.from_user.id):
        await callback.message.answer("✅ You are already registered.\nSiz allaqachon ro'yxatdan o'tgansiz.")
        await state.clear()
        return

    await callback.message.answer(get_text(lang, 'welcome_message'))
    await callback.message.answer(get_text(lang, 'prompt_name'))
    await state.set_state(RegistrationStates.waiting_for_name)
    await callback.answer()