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
from config import BASE_URL


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


def confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "confirm_true":
        params = {
            "telegram_id": update.effective_user.id,
            "first_name":  context.user_data['first_name'],
            "last_name" : context.user_data['last_name'],
            "phone":context.user_data['phone'],
            "avatar":context.user_data['photo_url']
        }

        requests.post(url=BASE_URL, json=params)
        query.edit_message_caption(
        caption=(
            "✅ <b>Ma'lumotlaringiz tasdiqlandi!</b>\n\n"
            "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi 🎉"
            ),
            parse_mode="HTML"
        )
        context.user_data.clear()
        return ConversationHandler.END

    query.edit_message_caption(
    caption=(
        "🔁 <b>Qayta kiritish</b>\n\n"
        "Iltimos, ism va familiyangizni qayta yuboring.\n"
        "Masalan: <code>Ali Valiyev</code>"
    ),
    parse_mode="HTML"
    )

    return Step.fullname


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Jarayon bekor qilindi.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END