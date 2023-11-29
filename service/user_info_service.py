from models.UserInfo import UserInfo
from repository.user_info_repository import UserInfoRepository


class UserInfoService:
    # Додавання даних юзера в таблицю бази даних users
    @staticmethod
    def create_user(user: UserInfo):
        return UserInfoRepository.create_user(user)

    # Отримання даних з таблиці users
    @staticmethod
    def get_user_by_id(user: UserInfo):
        return UserInfoRepository.get_user_by_id(user.id)

    # Оновлення даних в таблиці Users, при відсутності працює як create
    @staticmethod
    def update_user(user: UserInfo):
        db_user = UserInfoService.get_user_by_id(user)
        if db_user is None:
            UserInfoService.create_user(user)
        else:
            UserInfoRepository.update_user(user)

    # Видалення ланих з таблиці users
    @staticmethod
    def delete_user(user: UserInfo):
        UserInfoRepository.delete_user(user.id)