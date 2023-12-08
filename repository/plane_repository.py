import sqlite3

from db.db_init import DB_NAME
from models.Plane import Plane


class PlaneRepository:

    @staticmethod
    def get_by_id(plane_id):
        conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM plane WHERE id={plane_id}')
        plane = cursor.fetchone()

        cursor.close()
        conn.close()
        if plane is None:
            return plane
        else:
            return Plane.from_tuple(plane)