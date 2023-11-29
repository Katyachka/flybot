import sqlite3

from db.db_init import DB_NAME
from models.UserInfo import UserInfo


class UserInfoRepository:
    @staticmethod
    def create_user(user: UserInfo):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO userinfo (id, name, surname, gender, phone, email) '
                       f'VALUES (?, ?, ?, ?, ?, ?)',
                       (user.id, user.name, user.surname, user.gender, user.phone, user.email))

        id = cursor.lastrowid
        conn.commit()

        cursor.close()
        conn.close()
        return id


    # Отримання даних з таблиці userinfo
    @staticmethod
    def get_user_by_id(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM userinfo WHERE id={user_id}')
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return UserInfo.from_tuple(user)

    # Оновлення даних в таблиці userinfo
    @staticmethod
    def update_user(user: UserInfo):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'UPDATE userinfo '
                       f'SET (name, surname, gender, phone, email) = (?,?,?,?,?) '
                       f'WHERE id = {user.id}', (user.name, user.surname, user.gender, user.phone, user.email))

        conn.commit()

        cursor.close()
        conn.close()

    # Видалення ланих з таблиці userinfo
    @staticmethod
    def delete_user(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM userinfo '
                       f'WHERE id = \'{user_id}\'')

        conn.commit()

        cursor.close()
        conn.close()