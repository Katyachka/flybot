from models.User import User
from repository.user_repository import UserRepository


class UserService:

    # Додавання даних юзера в таблицю бази даних users
    @staticmethod
    def create_user(user: User):
        UserRepository.create_user(user)

    # Отримання даних з таблиці users
    @staticmethod
    def get_user_by_id(user: User):
        return UserRepository.get_user_by_id(user.id)

    # Оновлення даних в таблиці Users, при відсутності працює як create
    @staticmethod
    def update_user(user: User):
        db_user = UserService.get_user_by_id(user)
        if db_user is None:
            UserService.create_user(user)
        else:
            UserRepository.update_user(user)

    # Видалення ланих з таблиці users
    @staticmethod
    def delete_user(user: User):
        UserRepository.delete_user(user.id)