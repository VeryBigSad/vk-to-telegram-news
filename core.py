import logging
from os import getenv
from telegram.ext import Updater, CommandHandler
from telegram_commands import start, get_last_post, get_random_post
from user import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class App:
    user_list = {}
    updater = None

    @staticmethod
    def __init__():
        user = User(405521598)
        user.auth(getenv("username"), getenv("password"))

        App.user_list = {405521598: user}
        # TODO: implement DB functionality
        App.updater = Updater(getenv("token"))

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        return App.user_list.get(telegram_id)

    @staticmethod
    def start():
        dispatcher = App.updater.dispatcher

        # commands
        # TODO: add use of message_logger() func here, defined in telegram_commands.py
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("last_post", get_last_post))
        dispatcher.add_handler(CommandHandler("random_post", get_random_post))
        dispatcher.add_error_handler()
        # dispatcher.add_handler(CallbackContext)

        # Start the Bot
        App.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        App.updater.idle()

