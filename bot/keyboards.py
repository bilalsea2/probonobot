from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

CHANNEL_LINK = "https://t.me/pro_bonouz"

def language_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 Uzbek",   callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subscribe_kb(subscribe_text: str, check_text: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=subscribe_text, url=CHANNEL_LINK)
    kb.button(text=check_text, callback_data="check_sub")
    return kb.as_markup()


def gender_kb(lang: str) -> InlineKeyboardMarkup:
    labels = {
        'uz': ("Erkak", "Ayol"),
        'ru': ("Мужской", "Женский"),
        'en': ("Male", "Female"),
    }
    male, female = labels.get(lang, labels['en'])
    buttons = [
        [InlineKeyboardButton(text=male,   callback_data="gender_male")],
        [InlineKeyboardButton(text=female, callback_data="gender_female")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def fields_kb(lang: str) -> InlineKeyboardMarkup:
    # callback_data kept without spaces to be safe
    items = {
        "IELTS": {
            'uz': "IELTS",
            'ru': "IELTS",
            'en': "IELTS",
            'cb': "field_ielts"
        },
        "Mathematics": {
            'uz': "Matematika",
            'ru': "Математика",
            'en': "Mathematics",
            'cb': "field_mathematics"
        },
        "Economics": {
            'uz': "Iqtisodiyot",
            'ru': "Экономика",
            'en': "Economics",
            'cb': "field_economics"
        },
        "Engineering": {
            'uz': "Muhandislik",
            'ru': "Инженерия",
            'en': "Engineering",
            'cb': "field_engineering"
        },
        "MachineLearning": {
            'uz': "Sun'iy intellekt",
            'ru': "Машинное обучение",
            'en': "Machine Learning",
            'cb': "field_ml"
        },
    }

    kb = InlineKeyboardBuilder()
    for _, data in items.items():
        kb.button(text=data.get(lang, data['en']), callback_data=data['cb'])
    kb.adjust(1)
    return kb.as_markup()