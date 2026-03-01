from telegram import (
    Update,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import CallbackContext, ConversationHandler
from handlers.buttons.auth_buttons import confirm_button

from state import Step
import requests
from config import BASE_URL, BASE_SITE_URL, BASE_URL_REFRESH


def register(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.message.delete()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Ism familiyangizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )

    return Step.fullname


def get_fullname(update: Update, context: CallbackContext):
    full_name = update.message.text.split()

    if len(full_name) != 2:
        update.message.reply_html(
            "❗ <b>Xatolik</b>\n\n"
            "Iltimos, ism va familiyangizni to‘liq kiriting.\n"
            "Masalan: <code>Abdurauf Nasrullayev</code>"
        )       
        return Step.fullname
 
    context.user_data['first_name'] = full_name[0].title()
    context.user_data['last_name'] = full_name[1].title()

    update.message.reply_html(
    "📱 <b>Telefon raqam</b>\n\n"
    "Quyidagi tugma orqali kontaktingizni yuboring 👇",

    reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    )

    return Step.phone


def get_phone(update: Update, context: CallbackContext):
    if update.message.contact:
        context.user_data["phone"] = update.message.contact.phone_number
    else:
        context.user_data["phone"] = update.message.text

    update.message.reply_text(
        "Avatar rasmingizni yuboring:",
        reply_markup=ReplyKeyboardRemove()
    )

    return Step.avatar


def get_avatar(update: Update, context: CallbackContext): 
    if not update.message.photo:
        update.message.reply_text(
            "❗ <b>Xatolik</b>\n\n"
            "Iltimos, avatar rasmingizni yuboring.",
            parse_mode="HTML"
        )

        return Step.avatar
    file_id = update.message.photo[-1].file_id
    context.user_data['photo_url'] = file_id 

    caption = (
    "📋 <b>Ma'lumotlaringizni tasdiqlang</b>\n\n"
    f"👤 <b>Ism:</b> {context.user_data['first_name'].title()}\n"
    f"👤 <b>Familiya:</b> {context.user_data['last_name'].title()}\n"
    f"📱 <b>Telefon:</b> {context.user_data['phone']}\n\n"
    "Ma'lumotlar to'g'rimi?"
    )

    update.message.reply_photo(
        photo=file_id,
        caption=caption,
        reply_markup=confirm_button(),
        parse_mode="HTML"
    )

    return Step.confirm


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

user_tokens = {}

def confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = update.effective_user

    # Username tekshiruv
    if not user.username:
        query.edit_message_caption(
            caption=(
                "❗ <b>Xatolik</b>\n\n"
                "Iltimos, Telegram username o‘rnating."
            ),
            parse_mode="HTML"
        )
        return ConversationHandler.END

    if query.data != "confirm_true":
        return ConversationHandler.END

    params = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": context.user_data.get('first_name'),
        "last_name": context.user_data.get('last_name'),
        "phone_number": context.user_data.get('phone'),
        "avatar": context.user_data.get('photo_url')
    }

    try:
        response = requests.post(url=BASE_URL, json=params, timeout=10)

        if response.status_code != 200:
            query.edit_message_caption(
                caption="❌ Server javobida xatolik yuz berdi.",
                parse_mode="HTML"
            )
            return ConversationHandler.END

        data = response.json()

        access = data.get("access")
        refresh = data.get("refresh")

        if not access or not refresh:
            query.edit_message_caption(
                caption="❌ Token olinmadi.",
                parse_mode="HTML"
            )
            return ConversationHandler.END

        user_tokens[user.id] = {
            "access": access,
            "refresh": refresh
        }
        site_url = f"{BASE_SITE_URL}?token={access}"


        keyboard = [
            [InlineKeyboardButton("🌐 Saytga kirish", url=site_url)]
        
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_caption(
            caption=(
                "✅ <b>Muvaffaqiyatli!</b>\n\n"
                "Ro‘yxatdan o‘tish yakunlandi 🎉\n\n"
                "Quyidagi tugma orqali saytga o‘ting:"
            ),
            reply_markup=reply_markup,
            parse_mode="HTML"
        ),
        update.message.reply_text(
            "Saytni yangilash uchun /start buyrug'ini yuboring."
        )

        
        context.user_data.clear()

        return ConversationHandler.END

    except requests.exceptions.RequestException:
        query.edit_message_caption(
            caption="❌ Server bilan bog‘lanishda xatolik yuz berdi.",
            parse_mode="HTML"
        )
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Jarayon bekor qilindi.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END



user_tokens = {}

def login_user(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    telegram_id = update.effective_user.id

    response = requests.post(
        url=BASE_URL,
        json={"telegram_id": telegram_id}
    )

    if response.status_code != 200:
        query.edit_message_text("❌ Login amalga oshmadi.")
        return

    data = response.json()

    access = data["access"]
    refresh = data["refresh"]

    user_tokens[telegram_id] = {
        "access": access,
        "refresh": refresh
    }

    query.edit_message_text(
        "✅ Muvaffaqiyatli login qilindi!\n\n"
        "Endi tizimdan foydalanishingiz mumkin."
    )