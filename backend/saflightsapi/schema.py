from email.policy import default
import graphene
from graphene_django import DjangoObjectType
from .models import Aircraft, Airport, Arrival, Departure, Flight
from .service import getFlightsFromAirport, getFlightsToAirport

class AirportType(DjangoObjectType):
    class Meta:
        model = Airport
        fields = (
            'icao_code',
            'iata_code',
            'name',
            'city',
            'country',
            'latitude_deg',
            'longitude_deg',
            'elevation',
            'image_url',
        )

class AircraftType(DjangoObjectType):
    class Meta:
        model = Aircraft
        fields = (
            'category',
            'type',
            'icao',
        )


class FlightType(DjangoObjectType):
    class Meta:
        model = Flight
        fields = (
            'number',
            'iata_code',
            'icao_code',
            'date',
            'status',
            'airline',
            'departure',
            'arrival',
        )

class DepartureType(DjangoObjectType):
    class Meta:
        model = Departure
        fields = (
            'airport',
            'terminal',
            'gate',
            'baggage',
            'time_delay',
            'time_scheduled',
            'time_estimated',
            'time_actual',
            'estimated_runway',
            'actual_runway',
        )

class ArrivalType(DjangoObjectType):
    class Meta:
        model = Arrival
        fields = (
            'airport',
            'terminal',
            'gate',
            'baggage',
            'time_delay',
            'time_scheduled',
            'time_estimated',
            'time_actual',
            'estimated_runway',
            'actual_runway',
        )

class Query(graphene.ObjectType):

    airports_in_country = graphene.List(AirportType, country=graphene.String(required=False))
    all_airports = graphene.List(AirportType)
    airport = graphene.Field(AirportType, icao=graphene.String(required=False))
    flights = graphene.List(FlightType, icao=graphene.String(required=True))
    all_flights = graphene.List(FlightType)
    departures = graphene.List(FlightType, icao=graphene.String(required=True))
    arrivals = graphene.List(FlightType, icao=graphene.String(required=True))
    aircrafts = graphene.List(AircraftType)
    aircraft = graphene.Field(AircraftType, icao=graphene.String(required=True))

    def resolve_aircrafts(root, info):
        return Aircraft.objects.all()
    
    def resolve_aircraft(root, info, icao):
        return Aircraft.objects.get(icao=icao)

    def resolve_all_airports(root, info):
        return Airport.objects.all()

    def resolve_airports_in_country(root, info, country):
        if country:
            return Airport.objects.filter(country=country)
        else:
            return Airport.objects.all()
    
    def resolve_airport(root, info, icao):
        if icao:
            return Airport.objects.filter(icao_code=icao)
        else:
            return None

    def resolve_flights(root, info, icao):
        
        #getFlightsFromAirport(icao)
        #getFlightsToAirport(icao)

        airport = Airport.objects.get(icao_code=icao)
        departures = Flight.objects.filter(departure__airport=airport)
        arrivals = Flight.objects.filter(arrival__airport=airport)

        return departures | arrivals

    def resolve_departures(root, info, icao):
        airport = Airport.objects.get(icao_code=icao)
        flights = Flight.objects.filter(departure__airport=airport)
        return flights
    
    def resolve_arrivals(root, info, icao):
        airport = Airport.objects.get(icao_code=icao)
        flights = Flight.objects.filter(arrival__airport=airport)
        return flights

    def resolve_all_flights(root, info):
        return Flight.objects.all()

schema = graphene.Schema(query=Query)