from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import requests
from handlers.buttons.auth_buttons import register_button

from config import BASE_SITE_URL, BASE_URL_LOGIN

def start_bot(update: Update, context: CallbackContext):
    user = update.effective_user

    # 1. check-user
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/auth/check-user/",
        params={"telegram_id": user.id}
    )

    data = response.json()

    if not data['exists'] == True:
        update.message.reply_text(
            "Ro‘yxatdan o‘tish uchun tugmani bosing.",
            reply_markup=register_button()
        )
    else:
        login_response = requests.post(
            url=BASE_URL_LOGIN,
            json={"telegram_id": user.id}
        )

        if login_response.status_code != 200:
            update.message.reply_text("❌ Login xatosi.")
            return

        tokens = login_response.json()
        access = tokens["access"]

        # 3. Link beramiz
        site_url = f"{BASE_SITE_URL}?token={access}"

        keyboard = [
            [InlineKeyboardButton("🌐 Profilga o‘tish", url=site_url)]
        ]

        update.message.reply_text(
            "Profilingizga o‘tish uchun tugmani bosing 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
