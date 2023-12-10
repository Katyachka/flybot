class UserTicket:

    def __init__(self, id=None, user_id=None, ticket_id=None):
        self.id = id
        self.user_id = user_id
        self.ticket_id = ticket_id

    @staticmethod
    def from_tuple(user_ticket: tuple):
        if user_ticket is None:
            return user_ticket
        else:
            return UserTicket(id=user_ticket[0], user_id=user_ticket[1], ticket_id=user_ticket[2])
