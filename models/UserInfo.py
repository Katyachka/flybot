class UserInfo:

    def __init__(self, id=None, name=None, surname=None, gender=None, phone=None, email=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.gender = gender
        self.phone = phone
        self.email = email

    @staticmethod
    def from_tuple(user_info: tuple):
        if user_info is None:
            return user_info
        else:
            return UserInfo(id=user_info[0], name=user_info[1], surname=user_info[2],
                            gender=user_info[3], phone=user_info[4], email=user_info[5])
