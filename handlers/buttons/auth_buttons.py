from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def register_button():
    keyboard = [
        [InlineKeyboardButton(text="Royxatdan o'tish", callback_data="register")]
    ]

    return InlineKeyboardMarkup(keyboard)

def confirm_button():
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_true"),
            InlineKeyboardButton(text="🔄 Qayta kiritish", callback_data="confirm_false")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def login_button():
    keyboard = [
        [InlineKeyboardButton("🔐 Login qilish", callback_data="login_user")]
    ]
    return InlineKeyboardMarkup(keyboard)

