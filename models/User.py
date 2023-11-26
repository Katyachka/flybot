class User:

    def __init__(self, id=None, user_info_id=None, save_info=False):
        self.id = id
        self.user_info_id = user_info_id
        self.save_info = save_info

    @staticmethod
    def from_tuple(user: tuple):
        if user is None:
            return user
        else:
            return User(id=user[0], user_info_id=user[1], save_info=user[2])