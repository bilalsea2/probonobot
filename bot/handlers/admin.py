import logging
import shlex

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from bot.states.admin import AdminAddQuestion

from config import ADMIN_IDS
from bot.utils import (
    load_questions,
    add_question,
    delete_question_by_index,
)

router = Router()
logger = logging.getLogger(__name__)

def get_canonical_field_name(input_field: str) -> str | None:
    questions = load_questions()
    for field_name in questions.keys():
        if field_name.lower() == input_field.lower():
            return field_name
    return None

from aiogram.fsm.context import FSMContext
from bot.states.admin import AdminAddQuestion


@router.message(Command("admin_add_q"), F.from_user.id.in_(ADMIN_IDS))
async def start_admin_add_q(message: Message, state: FSMContext):
    await message.answer("🗂 Enter the field name (e.g., Machine Learning):")
    await state.set_state(AdminAddQuestion.waiting_for_field)

@router.message(AdminAddQuestion.waiting_for_field)
async def process_field_name(message: Message, state: FSMContext):
    field = message.text.strip()
    await state.update_data(field=field)
    await message.answer("✍️ Send the English version of the question:")
    await state.set_state(AdminAddQuestion.waiting_for_en_question)

@router.message(AdminAddQuestion.waiting_for_en_question)
async def process_en_question(message: Message, state: FSMContext):
    en_q = message.text.strip()
    await state.update_data(en_q=en_q)
    await message.answer("✍️ Send the Uzbek version of the question:")
    await state.set_state(AdminAddQuestion.waiting_for_uz_question)

@router.message(AdminAddQuestion.waiting_for_uz_question)
async def process_uz_question(message: Message, state: FSMContext):
    uz_q = message.text.strip()
    await state.update_data(uz_q=uz_q)
    await message.answer("📏 Max words allowed? (default: 200)")
    await state.set_state(AdminAddQuestion.waiting_for_max_words)

@router.message(AdminAddQuestion.waiting_for_max_words)
async def process_max_words(message: Message, state: FSMContext):
    try:
        max_words = int(message.text.strip())
        if not (1 <= max_words <= 500):
            raise ValueError
    except ValueError:
        await message.answer("❗ Invalid number. Please enter an integer between 1 and 500:")
        return

    data = await state.get_data()
    field = data['field']
    en_q = data['en_q']
    uz_q = data['uz_q']
    
    add_question(field, {"en": en_q, "uz": uz_q}, max_words)
    await message.answer(
        f"✅ Question added to <b>{field}</b>\n\n"
        f"🇬🇧 {en_q}\n🇺🇿 {uz_q}\n📝 Max words: {max_words}",
        parse_mode="HTML"
    )
    await state.clear()

@router.message(Command('admin_del_q'), F.from_user.id.in_(ADMIN_IDS))
async def admin_delete_question(message: Message):
    try:
        parts = shlex.split(message.text)
        if len(parts) < 3:
            await message.answer(
                "Usage: /admin_del_q <field> <index>\nExample: /admin_del_q \"Economics\" 1",
                parse_mode="HTML",
            )
            return

        field_input = parts[1]
        try:
            index = int(parts[2]) - 1
        except ValueError:
            await message.answer("Index must be an integer.", parse_mode="HTML")
            return

        field = get_canonical_field_name(field_input)
        if not field:
            fields = ", ".join(load_questions().keys())
            await message.answer(
                f"Field '<b>{field_input}</b>' not found. Available: {fields}",
                parse_mode="HTML",
            )
            return

        success = delete_question_by_index(field, index)
        if success:
            await message.answer(
                f"✅ Question {index+1} deleted from '<b>{field}</b>'.",
                parse_mode="HTML",
            )
            logger.info(f"Admin {message.from_user.id} deleted question {index+1} from {field}")
        else:
            await message.answer(
                f"Failed to delete. Field '<b>{field}</b>' or index {index+1} not found.",
                parse_mode="HTML",
            )

    except Exception as e:
        await message.answer(f"An unexpected error occurred: {e}", parse_mode="HTML")
        logger.exception("Error in admin_delete_question")

@router.message(Command('admin_list_q'), F.from_user.id.in_(ADMIN_IDS))
async def admin_list_questions(message: Message):
    try:
        parts = shlex.split(message.text)
        if len(parts) < 2:
            await message.answer(
                "Usage: /admin_list_q <field>\nExample: /admin_list_q \"IELTS\"",
                parse_mode="HTML",
            )
            return

        field_input = parts[1]
        field = get_canonical_field_name(field_input)
        if not field:
            fields = ", ".join(load_questions().keys())
            await message.answer(
                f"Field '<b>{field_input}</b>' not found. Available: {fields}",
                parse_mode="HTML",
            )
            return

        qs = load_questions().get(field, [])
        if not qs:
            await message.answer(
                f"No questions found for '<b>{field}</b>'.",
                parse_mode="HTML",
            )
            return

        response = f"📝 Questions for '<b>{field}</b>':\n"
        for i, q in enumerate(qs):
            response += f"{i+1}. {q['q']} (Max words: {q.get('max_words', 200)})\n"
        await message.answer(response, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"An unexpected error occurred: {e}", parse_mode="HTML")
        logger.exception("Error in admin_list_questions")