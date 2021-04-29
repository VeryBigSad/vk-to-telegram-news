class UserManager:

    @staticmethod
    def get_user_by_telegram_id(telegram_id):
        return App.user_list.get(telegram_id)


