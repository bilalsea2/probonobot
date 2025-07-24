import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards import language_kb, subscribe_kb
from bot.localization import get_text
from bot.utils import check_channel_subscription, is_user_registered
from bot.states.registration import RegistrationStates
from config import CHANNEL_ID

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Please choose your language:\nIltimos, tilingizni tanlang:\nПожалуйста, выберите язык:",
        reply_markup=language_kb()
    )

@router.callback_query(F.data.in_({'lang_uz', 'lang_en', 'lang_ru'}))
async def select_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split('_')[1]
    await state.update_data(lang=lang)
    await callback.message.edit_text(get_text(lang, 'language_selected'))

    if not await check_channel_subscription(callback.bot, callback.from_user.id, CHANNEL_ID):
        await callback.message.answer(
            get_text(lang, 'not_subscribed'),
            reply_markup=subscribe_kb(
                get_text(lang, 'subscribe_btn'),
                get_text(lang, 'check_btn')
            )
        )
        return

    if is_user_registered(callback.from_user.id):
        await callback.message.answer("✅ You are already registered.\nSiz allaqachon ro'yxatdan o'tgansiz.")
        await state.clear()
        return

    await callback.message.answer(get_text(lang, 'welcome_message'))
    await callback.message.answer(get_text(lang, 'prompt_name'))
    await state.set_state(RegistrationStates.waiting_for_name)
    await callback.answer()

@router.callback_query(F.data == "check_sub")
async def recheck_sub(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang", "en")
    if await check_channel_subscription(callback.bot, callback.from_user.id, CHANNEL_ID):
        await callback.message.edit_text(get_text(lang, 'thanks_for_sub'))
        await callback.message.answer(get_text(lang, 'welcome_message'))
        await callback.message.answer(get_text(lang, 'prompt_name'))
        await state.set_state(RegistrationStates.waiting_for_name)
    else:
        await callback.answer(get_text(lang, 'still_not_subscribed'), show_alert=True)