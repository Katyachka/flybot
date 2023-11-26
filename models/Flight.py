class Flight:

    def __init__(self, id=None, plane_id=None, departure=None, arrival=None, departure_date_time=None,
                 arrival_date_time=None, duration=None, cost_base=0, cost_regular=0, cost_plus=0):
        self.id = id
        self.plane_id = plane_id
        self.departure = departure
        self.arrival = arrival
        self.departure_date_time = departure_date_time
        self.arrival_date_time = arrival_date_time
        self.duration = duration
        self.cost_base = cost_base
        self.cost_regular = cost_regular
        self.cost_plus = cost_plus
