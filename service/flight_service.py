from datetime import datetime, time, timedelta

from models.Flight import Flight
from models.FlightModel import FlightModel
from repository.flight_repository import FlightRepository
from service.plane_service import PlaneService


class FlightService:

    @staticmethod
    def get_all():
        flights = FlightRepository.get_all()
        return FlightService.convert_to_models(flights)

    @staticmethod
    def get_with_departure_city(city):
        flights = FlightService.get_all()
        return list(filter(lambda flight: flight.departure == city, flights))

    @staticmethod
    def get_by_flight(flight: Flight, equals=True):
        flights = FlightService.get_all()

        if flight.departure_date_time:
            if equals:
                result = list(filter(lambda fgt: fgt.departure == flight.departure and fgt.arrival == flight.arrival
                                                 and FlightService.date_equals(fgt.departure_date_time,
                                                                               datetime.combine(flight.departure_date_time, time())),
                                     flights))
            else:
                result = list(filter(lambda fgt: fgt.departure == flight.departure and fgt.arrival == flight.arrival
                                                 and fgt.departure_date_time >= datetime.combine(flight.departure_date_time, time()) - timedelta(weeks=1)
                                                 and fgt.departure_date_time <= datetime.combine(flight.departure_date_time, time()) + timedelta(weeks=1), flights))
        else:
            result = list(filter(lambda fgt: fgt.departure == flight.departure and fgt.arrival == flight.arrival, flights))

        return result

    @staticmethod
    def date_equals(date1: datetime, date2: datetime):
        return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day

    @staticmethod
    def get_by_id(flight_id):
        return FlightService.convert_to_model(FlightRepository.get_by_id(flight_id))

    @staticmethod
    def convert_to_models(flights: list):
        flights_models = []
        for flight in flights:
            flights_models.append(FlightService.convert_to_model(flight))
        return flights_models

    @staticmethod
    def convert_to_model(flight: Flight):
        plane = PlaneService.get_by_id(flight.plane_id)
        return FlightModel(id=flight.id, plane=plane, departure=flight.departure, arrival=flight.arrival,
                           departure_date_time=flight.departure_date_time, arrival_date_time=flight.arrival_date_time,
                           duration=flight.duration, cost_base=flight.cost_base, cost_regular=flight.cost_regular,
                           cost_plus=flight.cost_plus)
