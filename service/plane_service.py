from repository.plane_repository import PlaneRepository


class PlaneService:

    @staticmethod
    def get_by_id(plane_id):
        return PlaneRepository.get_by_id(plane_id)