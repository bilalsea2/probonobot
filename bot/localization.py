MESSAGES = {
    'en': {
        'language_selected': "You have selected English.",
        'not_subscribed': "Please subscribe to our channel to continue: {channel_link}\nAfter subscribing, type /start again.",
        'welcome_message': "Welcome to the registration bot!",
        'prompt_name': "Please enter your full name:",
        'invalid_name_empty': "Name cannot be empty. Please enter your full name:",
        'prompt_age': "Please enter your age (e.g., 25):",
        'invalid_age': "Invalid age. Please enter a number between 1 and 99.",
        'prompt_gender': "Please select your gender:",
        'gender_male_label': "Male",
        'gender_female_label': "Female",
        'gender_other_label': "Other",
        'gender_selected': "You have selected: {gender}",
        'invalid_gender_input': "Please use the buttons to select your gender.",
        'prompt_field': "Please select your field of interest:",
        'field_selected': "You have selected: {field}",
        'invalid_field_input': "Please use the buttons to select your field of interest.",
        'question_prompt': "Question {question_num}: {question}",
        'empty_answer': "Your answer cannot be empty. Please provide an answer.",
        'answer_too_long': "Your answer is too long. Please keep it under {max_words} words.",
        'registration_complete': "Registration complete! Thank you.",
        'csv_save_error': "An error occurred while saving your data. Please try again later.",
        'telegram_notification_error': "An error occurred while sending notification. Please contact support."
    },
    'uz': {
        'language_selected': "Siz O'zbek tilini tanladingiz.",
        'not_subscribed': "Davom etish uchun iltimos kanalimizga obuna bo'ling: {channel_link}\nObuna bo'lganingizdan so'ng, /start buyrug'ini qayta yuboring.",
        'welcome_message': "Ro'yxatdan o'tish botiga xush kelibsiz!",
        'prompt_name': "Iltimos, ism-sharifingizni kiriting:",
        'invalid_name_empty': "Ism-sharif bo'sh bo'lishi mumkin emas. Iltimos, ism-sharifingizni kiriting:",
        'prompt_age': "Iltimos, yoshingizni kiriting (masalan, 25):",
        'invalid_age': "Noto'g'ri yosh. Iltimos, 1 dan 99 gacha bo'lgan son kiriting.",
        'prompt_gender': "Iltimos, jinsingizni tanlang:",
        'gender_male_label': "Erkak",
        'gender_female_label': "Ayol",
        'gender_other_label': "Boshqa",
        'gender_selected': "Siz tanladingiz: {gender}",
        'invalid_gender_input': "Iltimos, jinsingizni tanlash uchun tugmachalardan foydalaning.",
        'prompt_field': "Iltimos, qiziqish sohangizni tanlang:",
        'field_selected': "Siz tanladingiz: {field}",
        'invalid_field_input': "Iltimos, qiziqish sohangizni tanlash uchun tugmachalardan foydalaning.",
        'question_prompt': "Savol {question_num}: {question}",
        'empty_answer': "Javobingiz bo'sh bo'lishi mumkin emas. Iltimos, javob bering.",
        'answer_too_long': "Javobingiz juda uzun. Iltimos, uni {max_words} so'zdan oshirmang.",
        'registration_complete': "Ro'yxatdan o'tish yakunlandi! Rahmat.",
        'csv_save_error': "Ma'lumotlaringizni saqlashda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.",
        'telegram_notification_error': "Xabar yuborishda xatolik yuz berdi. Iltimos, yordam uchun murojaat qiling."
    }
}

def get_text(lang: str, key: str) -> str:
    return MESSAGES.get(lang, MESSAGES['en']).get(key, f"Error: Text not found for '{key}' in '{lang}'")
