class Plane:

    def __init__(self, id=None, model=None, passengers=0, layout=None, seat_in_row=0):
        self.id = id
        self.model = model
        self.passengers = passengers
        self.layout = layout
        self.seat_in_row = seat_in_row

    @staticmethod
    def from_tuple(plane: tuple):
        if plane is None:
            return plane
        else:
            return Plane(id=plane[0], model=plane[1], passengers=plane[2], layout=plane[3], seat_in_row=plane[4])
