class Ticket:

    def __init__(self, id=None, flight_id=None, plane_id=None, seat_id=None):
        self.id = id
        self.flight_id = flight_id
        self.plane_id = plane_id
        self.seat_id = seat_id

    @staticmethod
    def from_tuple(ticket: tuple):
        if ticket is None:
            return ticket
        else:
            return Ticket(id=ticket[0], flight_id=ticket[1], plane_id=ticket[2], seat_id=ticket[3])
