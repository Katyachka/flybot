class Plane:

    def __init__(self, id=None, model=None, passengers=0, layout=None):
        self.id = id
        self.model = model
        self.passengers = passengers
        self.layout = layout

    @staticmethod
    def from_tuple(plane: tuple):
        if plane is None:
            return plane
        else:
            return Plane(id=plane[0], model=plane[1], passengers=plane[2], layout=plane[3])
