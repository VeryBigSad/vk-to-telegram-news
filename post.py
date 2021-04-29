import logging

from utils import remove_escape_chars

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Post:
    def __init__(self, text='', post_type=None, attachments=None, author_name=None, like_count=0, comment_count=0):
        self.text = text
        self.post_type = post_type
        self.attachments = [] if attachments is None else attachments
        self.author_name = author_name
        self.like_count = like_count
        self.comment_count = comment_count

    def get_message_text(self):
        # return self.text + author sign
        a = f'{remove_escape_chars(self.text)}\n\n_{remove_escape_chars(self.author_name)}_' \
            if self.text != '' else f'_{remove_escape_chars(self.author_name)}_'
        return a
