from models.Ticket import Ticket
from repository.ticket_repository import TicketRepository


class TicketService:

    @staticmethod
    def create_ticket(ticket: Ticket):
        return TicketRepository.create_ticket(ticket)

    @staticmethod
    def get_ticket(ticket_id):
        return TicketRepository.get_ticket(ticket_id)