import sqlite3

from db.db_init import DB_NAME
from models.Ticket import Ticket
from models.User import User
from models.UserTicket import UserTicket


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

    @staticmethod
    def get_user_tickets(user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM user_ticket WHERE userId={user_id}')
        user_tickets = cursor.fetchall()

        cursor.close()
        conn.close()
        return [UserTicket.from_tuple(user_ticket) for user_ticket in user_tickets]