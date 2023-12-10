from models.Ticket import Ticket
from models.User import User
from repository.user_ticket_repository import UserTicketRepository
from service.ticket_service import TicketService


class UserTicketService:

    @staticmethod
    def create_user_ticket(user: User, ticket: Ticket):
        UserTicketRepository.create_user_ticket(ticket, user)

    @staticmethod
    def get_user_tickets(user_id):
        user_tickets = UserTicketRepository.get_user_tickets(user_id)
        tickets = []
        for user_ticket in user_tickets:
            tickets.append(TicketService.get_ticket(user_ticket.ticket_id))
        return tickets
