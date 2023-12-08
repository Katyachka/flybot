import sqlite3

from db.db_init import DB_NAME
from models.Seat import Seat


class SeatRepository:

    @staticmethod
    def get_all_by_flight_id(flight_id):
        conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM seat WHERE flightId={flight_id}')
        seats = cursor.fetchall()

        cursor.close()
        conn.close()
        if seats is None:
            return seats
        else:
            return [Seat.from_tuple(seat) for seat in seats]

    @staticmethod
    def create_seat(seat: Seat):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO seat (number, userInfoId, flightId, luggage_regular, luggage_plus) '
                       f'VALUES (?, ?, ?, ?, ?)',
                       (seat.number, seat.user_info_id, seat.flight_id, seat.luggage_regular, seat.luggage_plus))

        id = cursor.lastrowid
        conn.commit()

        cursor.close()
        conn.close()
        return id
