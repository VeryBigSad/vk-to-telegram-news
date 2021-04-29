from datetime import datetime
import logging

import vk_api
from post import Post

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class User:
    def __init__(self, telegram_user_id, vk_session_instance=None, channel_id=None):
        self.telegram_user_id = telegram_user_id
        self.channel_id = channel_id
        self.vk_session_instance = vk_session_instance
        self.last_time_newsfeed_checked = -1
        self.cached_newsfeed = None

    def auth(self, username, password):
        self.vk_session_instance = vk_api.VkApi(username, password)
        self.vk_session_instance.auth(token_only=True)

    def get_newsfeed(self):
        if datetime.now().timestamp() - self.last_time_newsfeed_checked >= 15:
            self.cached_newsfeed = self.__get_newsfeed_via_method()
            self.last_time_newsfeed_checked = datetime.now().timestamp()
        return self.cached_newsfeed

    def __get_newsfeed_via_method(self):
        """gets feed from VK and converts every convertable post into Post object
        :returns list of Post objects"""

        newsfeed_method = self.vk_session_instance.method("newsfeed.get", {"return_banned": "0",
                                                                           "filters": "post", "fields": "name"})
        news = []

        for i in newsfeed_method["items"]:
            ignore_post = False
            group_or_profile_obj = [j for j in newsfeed_method['groups' if i.get("source_id") < 0 else 'profiles']
                                    if j.get("id") == (abs(i.get("source_id")))][0]
            # TODO: check marked_as_ads and ignore those posts that are

            new_post = Post(text=i.get("text"),
                            author_name=group_or_profile_obj.get("name", str(group_or_profile_obj.get("first_name")) +
                                                                 " " + str(group_or_profile_obj.get("last_name"))),
                            like_count=i.get("likes").get("count"), comment_count=i.get("comments").get("count"),
                            owner_id=group_or_profile_obj.get("id"), item_id=i.get("post_id"),
                            author_type='group' if i.get('source_id') < 0 else 'profile')

            for attach in i.get("attachments") if i.get("attachments") is not None else []:
                if attach.get("type") == 'photo':
                    new_post.attachments.append(attach.get(attach.get("type"))["sizes"][-1]["url"])
                elif attach.get("type") == 'link':
                    new_post.attachments.append(attach["link"]["url"])
                else:
                    logger.warning(f"Unknown attachment type: {attach.get('type')}, ignoring it...")
                    ignore_post = True
                    break

                if new_post.post_type is not None and new_post.post_type != attach.get("type"):
                    logger.error("2 ATTACHMENT TYPES IN 1 MESSAGE!!! ABORT")
                    ignore_post = True
                    break
                new_post.post_type = attach.get("type")
            if not ignore_post:
                news.append(new_post)

        return news
