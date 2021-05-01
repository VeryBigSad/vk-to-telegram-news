import logging

from utils import remove_escape_chars

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Post:
    # TODO: add .add_attachment(value) -> None: and use it in user.py when adding attachments to the post

    def __init__(self, text='', post_type=None, attachments=None, author_name=None, like_count=0, comment_count=0,
                 owner_id=0, item_id=0, author_type=None):
        self.text = text
        self.post_type = post_type
        self.attachments = [] if attachments is None else attachments
        self.author_name = author_name
        self.author_type = ''
        self.like_count = like_count
        self.comment_count = comment_count
        self.owner_id = owner_id
        self.item_id = item_id

    def add_attachment(self, value) -> None:
        """adds an attachment to the post.
        :arg value - link to the attachment (photo, whatever)"""
        self.attachments.append(value)

    def get_message_text(self):
        """combines author's name and posts's text into a string that we use as text in the telegram message"""
        return f'{remove_escape_chars(self.text)}\n\n_{remove_escape_chars(self.author_name)}_' \
            if self.text != '' else f'_{remove_escape_chars(self.author_name)}_'
