import json
import logging
import csv
import os
import re
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
import gspread
from google.oauth2.service_account import Credentials

from config import CHANNEL_ID, QUESTIONS_FILE, CSV_FILE

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(
    os.getenv("GOOGLE_CREDS_PATH", "google_credentials.json"),
    scopes=SCOPES
)
gs_client = gspread.authorize(creds)
SPREADSHEET_ID = "1BllNn4StB93-oHIFGkL5UAeL1xxlb-ZoP00uFbV48x4"
sheet = gs_client.open_by_key(SPREADSHEET_ID).sheet1

async def check_channel_subscription(bot: Bot, user_id: int, channel_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except TelegramBadRequest as e:
        logger.warning(f"Could not get chat member for user {user_id} in channel {channel_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error checking channel subscription for user {user_id}: {e}")
        return False

def load_questions() -> dict:
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding {QUESTIONS_FILE}. It might be corrupted.")
        return {}

def save_questions(questions: dict):
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)
        logger.error(f"Error decoding {QUESTIONS_FILE}. It might be corrupted.")
        return {}

def save_questions(questions: dict):
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

def add_question(field: str, q_text: str | dict, max_words: int = 200):
    questions = load_questions()
    if field not in questions:
        questions[field] = []

    if isinstance(q_text, str):  # backward-compatible
        q_text = {"en": q_text, "uz": q_text}

    questions[field].append({'q': q_text, 'max_words': max_words})
    save_questions(questions)

## For future use, if you want to update a question by index
# def update_question_by_index(category: str, index: int, new_question: dict, max_words: int = 200):
#     data = load_questions()
#     if category in data and 0 <= index < len(data[category]):
#         data[category][index] = {
#             "q": new_question,
#             "max_words": max_words
#         }
#         save_questions(data)
#         return True
#     return False


def delete_question_by_index(field: str, index: int) -> bool:
    questions = load_questions()
    if field in questions and 0 <= index < len(questions[field]):
        del questions[field][index]
        save_questions(questions)
        return True
    return False


# --- Google Sheets Integration ---

async def append_to_google_sheets(record : dict):

    fieldnames = [
        'timestamp', 'user_id', 'telegram_username', 'name', 'age',
        'gender', 'selected_field',
        'q1_question', 'q1_answer',
        'q2_question', 'q2_answer',
        'q3_question', 'q3_answer',
        'q4_question', 'q4_answer',
        'language_used'
    ]

    row_data = {
        'timestamp': record.get('timestamp'),
        'user_id': record.get('user_id'),
        'telegram_username': record.get('telegram_username', ''),
        'name': record.get('name'),
        'age': record.get('age'),
        'gender': record.get('gender', ''),
        'selected_field': record.get('field'),
        'language_used': record.get('language'),
    }

    # Assume record['answers'] is a dict like:
    # { 'q1': {'question': '…', 'answer': '…'}, … }
    answers_dict = record.get('answers', {})
    for i in range(1, 5):  # up to 4 questions
        q_key = f'q{i}'
        ans_data = answers_dict.get(q_key, {})
        row_data[f'q{i}_question'] = ans_data.get('question', '')
        row_data[f'q{i}_answer']   = ans_data.get('answer', '')

    # 3) Build a list in the correct order and append:
    row = [ row_data.get(col, '') for col in fieldnames ]
    
    try:
        sheet.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        logger.error(f"Failed writing to Google Sheets: {e}")

    return True


# --- CSV Integration ---
async def append_to_csv(data: dict):
    fieldnames = [
        'timestamp', 'user_id', 'telegram_username', 'name', 'age',
        'gender', 'selected_field', 
        'q1_question', 'q1_answer', 
        'q2_question', 'q2_answer', 
        'q3_question', 'q3_answer',
        'q4_question', 'q4_answer', 
        'language_used'
    ]

    row_data = {
        'timestamp': data.get('timestamp'),
        'user_id': data.get('user_id'),
        'telegram_username': data.get('telegram_username'),
        'name': data.get('name'),
        'age': data.get('age'),
        'gender': data.get('gender'),
        'selected_field': data.get('selected_field'),
        'language_used': data.get('language_used')
    }

    answers_dict = data.get('answers', {})
    for i in range(1, 5): # Max 4 questions
        q_key = f'q{i}'
        ans_data = answers_dict.get(q_key, {})
        row_data[f'q{i}_question'] = ans_data.get('question', '')
        row_data[f'q{i}_answer'] = ans_data.get('answer', '')

    try:
        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader() # Write header only if file is new
            writer.writerow(row_data)
        logger.info(f"Row appended to CSV: {row_data}")
    except Exception as e:
        logger.error(f"Error appending to CSV file: {e}")
        raise # Re-raise to be handled by caller

def is_user_registered(user_id: int) -> bool:
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('user_id') == str(user_id):
                return True
    return False


# --- Telegram Notification ---
def escape_markdown_v2(text: str) -> str:
    """Helper to escape characters for MarkdownV2."""
    # List of characters to escape: _ * [ ] ( ) ~ ` > # + - = | { } . !
    # Escape backslash itself if it's not already escaping something
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def send_telegram_notification(bot: Bot, data: dict):
    answers_text = []
    answers_dict = data.get('answers', {})

    for i in range(1, 5):
        ans_data = answers_dict.get(f'q{i}')
        if ans_data:
            # Apply escaping to both question and answer
            question = escape_markdown_v2(ans_data['question'])
            answer = escape_markdown_v2(ans_data['answer'])
            answers_text.append(f"{i}. {question}: {answer}")

    answers_formatted = "\n".join(answers_text) if answers_text else "No answers provided."

    # Escape all parts of the message that are not intended as Markdown formatting
    user_name = escape_markdown_v2(data.get('name') or 'N/A')
    user_age = escape_markdown_v2(str(data.get('age') or 'N/A')) # Age is int, convert to str
    user_gender = escape_markdown_v2(data.get('gender') or 'N/A')
    selected_field = escape_markdown_v2(data.get('selected_field') or 'N/A')
    user_id = escape_markdown_v2(str(data.get('user_id') or 'N/A')) # User ID is int
    telegram_username = escape_markdown_v2(data.get('telegram_username') or 'N/A')
    timestamp = escape_markdown_v2(data.get('timestamp') or 'N/A')
    language_used = escape_markdown_v2(data.get('language_used') or 'N/A')

    message_text = f"""
    📝 New Registration {language_used}:

    👤 User: {user_name} {user_age}\\, {user_gender}
    💡 Field: {selected_field}
    🔗 User ID: `{user_id}` @{telegram_username}

    --- Answers ---
    {answers_formatted}

    📅 Timestamp: {timestamp}
    """

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message_text, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        raise # Re-raise to be handled by caller
