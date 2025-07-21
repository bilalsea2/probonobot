from email.mime import message
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.states.registration import RegistrationStates
from bot.keyboards import gender_kb, fields_kb
from bot.localization import get_text
from bot.utils import load_questions, append_to_csv, send_telegram_notification, append_to_google_sheets

router = Router()
logger = logging.getLogger(__name__)

@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')

    name = message.text.strip()
    if not name:
        await message.answer(get_text(lang, 'invalid_name_empty'))
        return

    await state.update_data(name=name)
    await message.answer(get_text(lang, 'prompt_age'))
    await state.set_state(RegistrationStates.waiting_for_age)

@router.message(RegistrationStates.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')

    try:
        age = int(message.text.strip())
        if not (0 < age < 100):
            raise ValueError
        await state.update_data(age=age)
        await message.answer(get_text(lang, 'prompt_gender'), reply_markup=gender_kb(lang))
        await state.set_state(RegistrationStates.waiting_for_gender)
    except ValueError:
        await message.answer(get_text(lang, 'invalid_age'))

@router.callback_query(RegistrationStates.waiting_for_gender, F.data.in_({'gender_male', 'gender_female', 'gender_other'}))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')

    gender_map = {
        'gender_male': get_text(lang, 'gender_male_label'),
        'gender_female': get_text(lang, 'gender_female_label'),
        'gender_other': get_text(lang, 'gender_other_label'),
    }
    gender = gender_map.get(callback.data)
    await state.update_data(gender=gender)
    await callback.message.edit_text(get_text(lang, 'gender_selected').format(gender=gender))

    await callback.message.answer(get_text(lang, 'prompt_field'), reply_markup=fields_kb(lang))
    await state.set_state(RegistrationStates.waiting_for_field)
    await callback.answer()

@router.message(RegistrationStates.waiting_for_gender)
async def process_gender_invalid_message(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')
    await message.answer(get_text(lang, 'invalid_gender_input'), reply_markup=gender_kb(lang))

@router.callback_query(RegistrationStates.waiting_for_field, F.data.startswith('field_'))
async def process_field(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')

    field = callback.data.split('_')[1]
    await state.update_data(selected_field=field, current_question_index=0, answers={})
    await callback.message.edit_text(get_text(lang, 'field_selected').format(field=field))

    await ask_next_question(callback.message, state, lang)
    await callback.answer()

@router.message(RegistrationStates.waiting_for_field)
async def process_field_invalid_message(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')
    await message.answer(get_text(lang, 'invalid_field_input'), reply_markup=fields_kb(lang))


async def ask_next_question(message: Message, state: FSMContext, lang: str):
    user_data = await state.get_data()
    field = user_data['selected_field']
    current_index = user_data['current_question_index']
    questions = load_questions().get(field, [])

    if current_index < len(questions):
        question_data = questions[current_index]
        question_text = question_data['q'].get(lang, question_data['q'].get('en'))
        await message.answer(get_text(lang, 'question_prompt').format(question_num=current_index + 1, question=question_text))
        await state.set_state(RegistrationStates.answering_questions)
    else:
        await complete_registration(message, state, lang)

@router.message(RegistrationStates.answering_questions)
async def process_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get('lang', 'en')
    field = user_data['selected_field']
    current_index = user_data['current_question_index']
    answers = user_data.get('answers', {})

    questions = load_questions().get(field, [])
    if current_index >= len(questions):
        # This should ideally not happen if flow is correct
        await complete_registration(message, state, lang)
        return

    question_data = questions[current_index]
    max_words = question_data.get('max_words', 200)

    answer_text = message.text.strip()
    if not answer_text:
        await message.answer(get_text(lang, 'empty_answer'))
        return

    if len(answer_text.split()) > max_words:
        await message.answer(get_text(lang, 'answer_too_long').format(max_words=max_words))
        return

    question_text = question_data['q'].get(lang, question_data['q'].get('en'))
    answers[f'q{current_index + 1}'] = {'question': question_text, 'answer': answer_text}

    await state.update_data(answers=answers, current_question_index=current_index + 1)

    await ask_next_question(message, state, lang)


async def complete_registration(message: Message, state: FSMContext, lang: str):
    user_data = await state.get_data()
    full_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': message.from_user.id,
        'telegram_username': message.from_user.username or 'N/A',
        'name': user_data.get('name'),
        'age': user_data.get('age'),
        'gender': user_data.get('gender'),
        'selected_field': user_data.get('selected_field'),
        'language_used': user_data.get('lang'),
        'answers': user_data.get('answers', {})
    }

    try:
        await append_to_csv(full_data)
        logger.info(f"Data for user {message.from_user.id} appended to CSV.")
    except Exception as e:
        logger.error(f"Failed to append data to CSV for user {message.from_user.id}: {e}")
        await message.answer(get_text(lang, 'csv_save_error'))

    try:
        await append_to_google_sheets(full_data)
        logger.info(f"Data for user {message.from_user.id} appended to Google Sheets.")
    except Exception as e:
        logger.error(f"Failed to append data to Google Sheets for user {message.from_user.id}: {e}")

    try:
        await send_telegram_notification(message.bot, full_data)
        logger.info(f"Notification sent for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification for user {message.from_user.id}: {e}")
        await message.answer(get_text(lang, 'telegram_notification_error'))

    await message.answer(get_text(lang, 'registration_complete'))
    await state.clear()
