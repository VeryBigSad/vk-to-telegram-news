class UserController:
    instance = None

    def __init__(self):
        UserController.instance = self
        self.user_list = {}

    @staticmethod
    def get_instance():
        return UserController.instance

    def get_user_by_telegram_id(self, telegram_id):
        return self.user_list.get(telegram_id)

    def add_user(self, user):
        self.user_list[user.telegram_user_id] = user



