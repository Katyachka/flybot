from models.UserInfo import UserInfo
from repository.user_info_repository import UserInfoRepository
from service.user_service import UserService


class UserInfoService:
    # Додавання даних юзера в таблицю бази даних users
    @staticmethod
    def create_user(user: UserInfo):
        return UserInfoRepository.create_user(user)

    # Отримання даних з таблиці users
    @staticmethod
    def get_user_by_id(user_id):
        return UserInfoRepository.get_user_by_id(user_id)

    # Оновлення даних в таблиці Users, при відсутності працює як create
    @staticmethod
    def update_user(user: UserInfo):
        db_user = UserInfoService.get_user_by_id(user.id)
        if db_user is None:
            UserInfoService.create_user(user)
        else:
            UserInfoRepository.update_user(user)

    # Видалення ланих з таблиці users
    @staticmethod
    def delete_user(user: UserInfo):
        UserInfoRepository.delete_user(user.id)

    @staticmethod
    def get_user_info_by_user_id(user_id):
        user = UserService.get_user_by_id(user_id)
        return UserInfoService.get_user_by_id(user.user_info_id)