from models.FlightModel import FlightModel
from models.Seat import Seat
from models.SeatModel import SeatModel
from repository.seat_repository import SeatRepository
from service.flight_service import FlightService
from service.user_info_service import UserInfoService


class SeatService:

    @staticmethod
    def get_all_by_flight_id(flight_id):
        seats = SeatRepository.get_all_by_flight_id(flight_id)
        seat_models = []
        for seat in seats:
            seat_models.append(SeatService.convert_to_model(seat))
        return seat_models

    @staticmethod
    def convert_to_model(seat: Seat):
        user_info = UserInfoService.get_user_by_id(seat.user_info_id)
        flight = FlightService.get_by_id(seat.flight_id)
        return SeatModel(id=seat.id, number=seat.number, user_info=user_info, flight=flight,
                         luggage_regular=seat.luggage_regular, luggage_plus=seat.luggage_plus)

    @staticmethod
    def has_flight_available_seats(flight: FlightModel):
        seats = SeatService.get_all_by_flight_id(flight.id)
        if len(seats) < flight.plane.passengers:
            return True
        else:
            return False

    @staticmethod
    def with_available_seats(flights):
        available = []
        for flight in flights:
            if SeatService.has_flight_available_seats(flight):
                available.append(flight)
        return available

    @staticmethod
    def create_seat(seat: Seat):
        return SeatRepository.create_seat(seat)
