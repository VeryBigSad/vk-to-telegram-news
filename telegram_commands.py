import ast
import json
import logging
import random

from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from user import User
from user_controller import UserController
from utils import send_typing_action, remove_escape_chars

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# TODO: make a proper /start command


def message_logger(update: Update, _: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} sent a message with text {update.message.text}")


def __reply_with_post(update, post):
    like_data = str(
        {'owner_id': post.owner_id if post.author_type == 'profile' else -post.owner_id, 'item_id': post.item_id,
         'like_count': post.like_count})
    # TODO: figure something out with comments
    comment_data = str('TODO')

    reply_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f'❤️ {post.like_count}', callback_data=like_data),
                                            InlineKeyboardButton(f'💬 {post.comment_count}',
                                                                 callback_data=comment_data)]])
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
    user_object = UserController.get_instance().get_user_by_telegram_id(update.effective_user.id)
    last_post = user_object.get_newsfeed()[0]
    __reply_with_post(update, last_post)


@send_typing_action
def get_random_post(update: Update, _: CallbackContext) -> None:
    """Send the user random post (from ~20-50 last posts) from his VK news feed"""
    user_object = UserController.get_instance().get_user_by_telegram_id(update.effective_user.id)
    post = random.choice(user_object.get_newsfeed())
    __reply_with_post(update, post)


def error_handler(update: object, context: CallbackContext) -> None:
    update.message.reply_markdown_v2(remove_escape_chars("Ой! Произошла какая-то ошибка...\n"
                                                         "Админу уже про нее заспамили!"))
    logger.error(f'Unknown error: {context.error.with_traceback(context.error.__traceback__)}')


def raise_error(update: Update, _: CallbackContext) -> None:
    raise Exception("/raise_error had been used. cool. this isn't an actual error btw")


def process_callback(update: Update, _: CallbackContext) -> int:
    """function which receives all callbacks there are"""
    # TODO: separate callbacks into different functions through Pattern in core.py Handler option
    query = update.callback_query
    query.answer()

    # probably very not safe
    data = ast.literal_eval(query.data)

    new_like_count = like_the_post(update.effective_user.id, data.get("owner_id"), data.get("item_id"))
    # might be a bug here, because string > 64 bytes
    callback_data = str({'owner_id': data.get("owner_id"), 'item_id': data.get("item_id"),
                         'like_count': new_like_count})

    reply_markup = query.message.reply_markup.inline_keyboard
    # TODO: remove this string here and replace it with constant from somewhere
    reply_markup[0][0] = InlineKeyboardButton(f'❤️ {new_like_count}', callback_data=callback_data)
    # TODO: replace caption with something else
    if query.message.text is None:
        query.edit_message_caption(caption=query.message.caption_markdown_v2, parse_mode='MarkdownV2',
                                   reply_markup=InlineKeyboardMarkup(reply_markup))
    else:
        query.edit_message_text(text=query.message.text_markdown_v2, parse_mode='MarkdownV2',
                                reply_markup=InlineKeyboardMarkup(reply_markup))

    return 0


# TODO: finish this & __unlike_the_post()
def like_the_post(telegram_id, owner_id, item_id) -> int:
    """likes the post with the telegram_id persons's account
    :returns new amount of likes"""
    user_object = UserController.get_instance().get_user_by_telegram_id(telegram_id)
    resp = user_object.vk_session_instance.method("likes.add", values={'type': 'post', 'owner_id': owner_id,
                                                                       'item_id': item_id})
    return resp.get("likes")


def __unlike_the_post(user_object: User, update: Update, _: CallbackContext) -> None:
    pass
