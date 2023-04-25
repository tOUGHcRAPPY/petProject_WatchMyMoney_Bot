from .bot import bot
from .handlers import *

from telegram.ext import (
    CommandHandler,
    Dispatcher, MessageHandler, Filters, CallbackQueryHandler,

)

dispatcher = Dispatcher(
    bot,
    workers=0,
    update_queue=None,
)

# Handle start command
dispatcher.add_handler(CommandHandler("start", start_handler))
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=main_message_handler))
dispatcher.add_handler(CallbackQueryHandler(callback=check_btn))
