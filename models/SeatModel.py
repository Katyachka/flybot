from models.Flight import Flight
from models.UserInfo import UserInfo


class SeatModel:

    def __init__(self, id=None, number=None, user_info=None, flight=None, luggage_regular=None, luggage_plus=None):
        self.id = id
        self.number = number
        self.user_info: UserInfo = user_info
        self.flight: Flight = flight
        self.luggage_regular = luggage_regular
        self.luggage_plus = luggage_plus
