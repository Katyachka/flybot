import sqlite3

from db.db_init import DB_NAME
from models.Ticket import Ticket
from models.User import User


class UserTicketRepository:

    @staticmethod
    def create_user_ticket(ticket: Ticket, user: User):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO user_ticket (userId, ticketId) '
                       f'VALUES (?, ?)',
                       (user.id, ticket.id))

        conn.commit()

        cursor.close()
        conn.close()