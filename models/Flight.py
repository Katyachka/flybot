from datetime import datetime


class Flight:

    def __init__(self, id=None, plane_id=None, departure=None, arrival=None, departure_date_time: datetime=None,
                 arrival_date_time: datetime=None, duration=None, cost_base=0, cost_regular=0, cost_plus=0):
        self.id = id
        self.plane_id = plane_id
        self.departure = departure
        self.arrival = arrival
        self.departure_date_time: datetime = departure_date_time
        self.arrival_date_time: datetime = arrival_date_time
        self.duration = duration
        self.cost_base = cost_base
        self.cost_regular = cost_regular
        self.cost_plus = cost_plus

    @staticmethod
    def from_tuple(flight):
        if flight is None:
            return flight
        else:
            return Flight(id=flight[0], plane_id=flight[1], departure=flight[2], arrival=flight[3],
                          departure_date_time=datetime.fromtimestamp(flight[4]),
                          arrival_date_time=datetime.fromtimestamp(flight[5]),
                          duration=flight[6], cost_base=flight[7], cost_regular=flight[8],
                          cost_plus=flight[9])
