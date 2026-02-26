from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from config import TOKEN
from handlers.command_handlers.start import start_bot
from handlers.message_handlers.message_handlers import register, get_fullname, get_avatar, get_phone, confirm, cancel
from state import Step


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_bot))

    register_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(register, pattern="^register")
        ],
        states={
            Step.fullname: [MessageHandler(Filters.text & ~Filters.command, get_fullname)],
            Step.phone: [MessageHandler(Filters.contact & ~Filters.command, get_phone)],
            Step.avatar: [MessageHandler(Filters.photo, get_avatar)],
            Step.confirm: [CallbackQueryHandler(confirm, r"^confirm_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        )
    
    dispatcher.add_handler(register_conv)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
