from models.Ticket import Ticket
from models.User import User
from repository.user_ticket_repository import UserTicketRepository


class UserTicketService:

    @staticmethod
    def create_user_ticket(user: User, ticket: Ticket):
        UserTicketRepository.create_user_ticket(ticket, user)