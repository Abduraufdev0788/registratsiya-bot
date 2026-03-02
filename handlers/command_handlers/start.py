from telegram import Update
from telegram.ext import CallbackContext
import requests
from handlers.buttons.auth_buttons import register_button
from config import BASE_URL
def start_bot(update: Update, context: CallbackContext):
    user = update.effective_user
    response = requests.get(
        url=BASE_URL,
        params={"telegram_id": user.id}
    )

    data = response.json()
    

    if data['status'] == "User not found":
        update.message.reply_text(
            "Ro‘yxatdan o‘tish uchun tugmani bosing.",
            reply_markup=register_button()
        )
    elif data["status"] == "success":
        update.message.reply_html(
            f"""<b>👤 Sizning ma'lumotlaringiz:</b>

🆔 <b>Telegram ID:</b> {data['user']['telegram_id']}
👤 <b>Username:</b> {data['user']['username']}
📛 <b>Ism:</b> {data['user']['first_name']}
📛 <b>Familiya:</b> {data['user']['last_name']}
📞 <b>Telefon:</b> {data['user']['phone_number']}"""


f"\n\n sizning kodingiz: <code>{data['code']}</code>"
)
    
    
