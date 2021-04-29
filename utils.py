from functools import wraps
import random
import time
from telegram import ChatAction


def remove_escape_chars(msg: str):
    return msg.replace('#', '\\#') \
        .replace('_', '\\_') \
        .replace('-', '\\-') \
        .replace('~', '\\~') \
        .replace('`', '\\`') \
        .replace('*', '\\*') \
        .replace('.', '\\.') \
        .replace('(', '\\(') \
        .replace(')', '\\)') \
        .replace('|', '\\|') \
        .replace('+', '\\+') \
        .replace('!', '\\!') \
        .replace('=', '\\=')


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        time.sleep(random.random())
        return func(update, context,  *args, **kwargs)

    return command_func


def apologize_if_error(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        try:
            return func(update, context, *args, **kwargs)
        except Exception:
            update.message.reply_markdown_v2("Ой! Произошла какая-то ошибка... ")
            # TODO: log

    return command_func


def telegram_command(func):
    """collection of decorators for a telegram function"""
    @wraps(func)
    @send_typing_action
    @apologize_if_error
    def command_func(update, context, *args, **kwargs):
        return func(update, context, *args, **kwargs)

    return command_func
