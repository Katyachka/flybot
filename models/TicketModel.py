from models.Flight import Flight
from models.Seat import Seat


class TicketModel:

    def __init__(self, id=None, flight=None, seat=None):
        self.id = id
        self.flight: Flight = flight
        self.seat: Seat = seat
