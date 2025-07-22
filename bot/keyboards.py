from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_kb():
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def gender_kb(lang: str):
    if lang == 'uz':
        buttons = [
            [InlineKeyboardButton(text="Erkak", callback_data="gender_male")],
            [InlineKeyboardButton(text="Ayol", callback_data="gender_female")],
            [InlineKeyboardButton(text="Boshqa", callback_data="gender_other")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Male", callback_data="gender_male")],
            [InlineKeyboardButton(text="Female", callback_data="gender_female")],
            [InlineKeyboardButton(text="Other", callback_data="gender_other")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def fields_kb(lang: str):
    if lang == 'uz':
        buttons = [
            [InlineKeyboardButton(text="IELTS", callback_data="field_IELTS")],
            [InlineKeyboardButton(text="Matematika", callback_data="field_Mathematics")],
            [InlineKeyboardButton(text="Iqtisodiyot", callback_data="field_Economics")],
            [InlineKeyboardButton(text="Aerokosmik Muhandislik", callback_data="field_Engineering")],
            [InlineKeyboardButton(text="Sun'iy Zako", callback_data="field_Machine Learning")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="IELTS", callback_data="field_IELTS")],
            [InlineKeyboardButton(text="Mathematics", callback_data="field_Mathematics")],
            [InlineKeyboardButton(text="Economics", callback_data="field_Economics")],
            [InlineKeyboardButton(text="Engineering", callback_data="field_Engineering")],
            [InlineKeyboardButton(text="Machine Learning", callback_data="field_Machine Learning")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)