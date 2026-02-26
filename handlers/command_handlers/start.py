from telegram import Update
from telegram.ext import CallbackContext
import requests
from handlers.buttons.auth_buttons import register_button

from config import BASE_URL

def start_bot(update:Update, context:CallbackContext):
    telegram_id = update.effective_user.id

    response = requests.get(url=BASE_URL, params={"telegram_id": telegram_id}).json()

    if response["status"] != "exists":
        update.message.reply_text(
            text = f"Assalomu Alaykum {update.effective_user.full_name}\nBotimizga xush kelibsiz\nlogin qilish uchun pastdagi tugmani bosing",
            reply_markup=register_button()
        )
    else:
        update.message.reply_text(
        text=(
            f"Assalomu alaykum {update.effective_user.full_name} 👋\n\n"
            "Siz allaqachon ro‘yxatdan o‘tgansiz ✅\n\n"
            "Profilingiz faol."
        )
    )
    
