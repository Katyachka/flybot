import sqlite3

from db.db_init import DB_NAME
from models.Flight import Flight


class FlightRepository:

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM flight')
        flights = cursor.fetchall()

        cursor.close()
        conn.close()
        if flights is None:
            return flights
        else:
            return [Flight.from_tuple(flight) for flight in flights]

    @staticmethod
    def get_by_id(flight_id):
        conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM flight WHERE id={flight_id}')
        flight = cursor.fetchone()

        cursor.close()
        conn.close()
        if flight is None:
            return flight
        else:
            return Flight.from_tuple(flight)