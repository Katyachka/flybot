class Seat:

    def __init__(self, id=None, number=None, user_info_id=None, flight_id=None, luggage_regular=None, luggage_plus=None):
        self.id = id
        self.number = number
        self.user_info_id = user_info_id
        self.flight_id = flight_id
        self.luggage_regular = luggage_regular
        self.luggage_plus = luggage_plus

    @staticmethod
    def from_tuple(seat):
        if seat is None:
            return seat
        else:
            return Seat(id=seat[0], number=seat[1], user_info_id=seat[2], flight_id=seat[3], luggage_regular=seat[4],
                        luggage_plus=seat[5])
