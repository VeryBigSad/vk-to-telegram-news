import logging
import random

from telegram import Update, ForceReply, InputMediaPhoto, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import CallbackContext

from core import App
from user import User
from utils import send_typing_action

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


@send_typing_action
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # update.message.reply_markdown_v2()
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def message_logger(update: Update, _: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} sent a message with text {update.message.text}")


def __reply_with_post(update, post):
    reply_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f'❤️ {post.like_count}', callback_data="TODO"),
                                            InlineKeyboardButton(f'💬 {post.comment_count}', callback_data="TODO")]])
    if len(post.attachments) >= 2:
        # TODO: choose the right media group
        to_send = [InputMediaPhoto(i, parse_mode='MarkdownV2') for i in post.attachments]
        to_send[0] = InputMediaPhoto(post.attachments[0], caption=post.get_message_text(), parse_mode='MarkdownV2')
        update.message.reply_media_group(to_send)
    else:
        if post.post_type == 'photo':
            update.message.reply_photo(post.attachments[0], caption=post.get_message_text(),
                                       parse_mode='MarkdownV2', reply_markup=reply_keyboard)
            # TODO: find the requested type of media and send it
        elif post.post_type is None:
            update.message.reply_markdown_v2(post.get_message_text(),
                                             reply_markup=reply_keyboard)


@send_typing_action
def get_last_post(update: Update, _: CallbackContext) -> None:
    """Send the user his last post from his VK news feed"""
    user_object = App.get_user_by_telegram_id(update.effective_user.id)
    last_post = user_object.get_newsfeed()[0]
    __reply_with_post(update, last_post)


@send_typing_action
def get_random_post(update: Update, _: CallbackContext) -> None:
    """Send the user random post (from ~20-50 last posts) from his VK news feed"""
    user_object = App.get_user_by_telegram_id(update.effective_user.id)
    post = random.choice(user_object.get_newsfeed())
    __reply_with_post(update, post)


def error_handler(update: Update, _: CallbackContext):
    print()
    pass


def __like_the_post(update: Update, _: CallbackContext) -> None:
    user_object = App.get_user_by_telegram_id(update.effective_user.id)
    post_owner_id = None
    post_id = None
    # TODO: finish this
    user_object.vk_session_instance.method("likes.add", values={'type': 'post', 'owner_id': '', '': ''})


# TODO: todo
def __unlike_the_post(user_object: User, update: Update, _: CallbackContext) -> None:
    pass

