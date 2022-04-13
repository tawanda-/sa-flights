import code
import graphene
from graphene_django import DjangoObjectType
from .models import Airport, Flight, FlightDetail
from .service import getFlights, getAirportFlights

class AirportType(DjangoObjectType):
    class Meta:
        model = Airport
        fields = (
            'icao_code',
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
            'iata_code',
            'icao_code',
            'date',
            'source_airport',
            'destination_airport',
            'status',
            'airline',
            'departure',
            'arrival',
        )

class FlightDetailType(DjangoObjectType):
    class Meta:
        model = FlightDetail
        fields = (
            'status',
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
    airport = graphene.List(FlightType, icao_code=graphene.String(required=True))
   
    def resolve_airports(root, info):
        return Airport.objects.all()

    def resolve_airport(root, info, icao_code):

        if( Flight.objects.all().count() > 0 ):
            q1 = Flight.objects.filter(source_airport=Airport.objects.get(icao_code=icao_code))
            q2 = Flight.objects.filter(destination_airport=Airport.objects.get(icao_code=icao_code))
            q3 = q1.union(q2)
            return q3
        else:
            getAirportFlights(icao_code)
            return Flight.objects.filter(source_airport=Airport.objects.get(icao_code=icao_code)).filter(destination_airport=Airport.objects.get(icao_code=icao_code))

schema = graphene.Schema(query=Query)