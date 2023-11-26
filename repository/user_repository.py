import sqlite3

from db.db_init import DB_NAME
from models.User import User


class UserRepository:

    @staticmethod
    def create_user(user: User):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO users (id, userInfoId, saveInfo) '
                       f'VALUES (?, ?, ?)',
                       (user.id, user.user_info_id, user.save_info))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM users WHERE id={user_id}')
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return User.from_tuple(user)

    @staticmethod
    def update_user(user: User):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'UPDATE users '
                       f'SET (userInfoId, saveInfo) = (?,?) '
                       f'WHERE id = {user.id}', (user.user_info_id, user.save_info))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM users '
                       f'WHERE id = \'{user_id}\'')

        conn.commit()

        cursor.close()
        conn.close()
