import sqlite3

from db.db_init import DB_NAME
from models.Ticket import Ticket


class TicketRepository:

    @staticmethod
    def create_ticket(ticket: Ticket):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO ticket (flightId, planeId, seatId) '
                       f'VALUES (?, ?, ?)',
                       (ticket.flight_id, ticket.plane_id, ticket.seat_id))

        id = cursor.lastrowid
        conn.commit()

        cursor.close()
        conn.close()
        return id

    @staticmethod
    def get_ticket(ticket_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM ticket WHERE id={ticket_id}')
        ticket = cursor.fetchone()

        cursor.close()
        conn.close()
        return Ticket.from_tuple(ticket)