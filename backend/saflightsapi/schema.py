from ast import Num
import graphene
from graphene_django import DjangoObjectType
from .models import Airport, Flight, FlightDetail

class AirportType(DjangoObjectType):
    class Meta:
        model = Airport
        fields = (
            'iata_code',
            'name',
            'municipality',
            'latitude_deg',
            'longitude_deg',
            'elevation',
            'image_url',
        )

class FlightType(DjangoObjectType):
    class Meta:
        model = Flight
        fields = (
            'number',
            'date',
            'status',
            'airline',
        )

class FlightDetailType(DjangoObjectType):
    class Meta:
        model = FlightDetail
        fields = (
            'number',
            'status',
            'airport',
            'iata',
            'icao',
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

    airports = graphene.List(AirportType)
    airport = graphene.Field(AirportType, iata_code=graphene.String(required=True))

    flights = graphene.List(FlightType)
    flight = graphene.Field(FlightType, number=graphene.String(required=True))

    flightDetails = graphene.Field(FlightDetailType, number=graphene.String(required=True))
        
    def resolve_airports(root, info):
        return Airport.objects.all()

    def resolve_airport(root, info, iata_code):
        try:
            return Airport.objects.get(iata_code=iata_code)
        except Airport.DoesNotExist:
            return None

    def resolve_flights(root, info):
        return Flight.objects.all()

    def resolve_flight(root, info, number):
        try:
            return Flight.objects.get(number=number)
        except Flight.DoesNotExist:
            return None

    def resolve_flightDetail(root, info, number):
        try:
            return FlightDetailType.objects.get(number=number)
        except FlightDetail.DoesNotExist:
            return None
    
schema = graphene.Schema(query=Query)