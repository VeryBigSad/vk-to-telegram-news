import logging
from os import getenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram_commands import get_last_post, get_random_post, error_handler, raise_error, process_callback
from user import User
from user_controller import UserController

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class App:
    instance = None

    def __init__(self):
        App.instance = self

        user = User(405521598)
        user.auth(getenv("VK-TO-TG-USERNAME"), getenv("VK-TO-TG-PASSWORD"))
        self.user_controller = UserController()
        self.user_controller.add_user(user)

        self.updater = Updater(getenv("VK-TO-TG-TOKEN"))
        logger.debug("App class initialized")

    @staticmethod
    def get_instance():
        return App.instance

    def start(self):
        dispatcher = self.updater.dispatcher

        # commands
        # TODO: add use of message_logger() func here, defined in telegram_commands.py
        # dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("last_post", get_last_post))
        dispatcher.add_handler(CommandHandler("random_post", get_random_post))

        dispatcher.add_handler(CallbackQueryHandler(callback=process_callback, pass_user_data=True, pass_chat_data=True,
                                                    pass_groups=True, pass_groupdict=True, pass_job_queue=True,
                                                    pass_update_queue=True))

        # TODO: add admin-only filter
        dispatcher.add_handler(CommandHandler("raise_error", raise_error))

        # dispatcher.add_error_handler(error_handler)
        # dispatcher.add_handler(CallbackContext)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

