from dataclasses import fields
import graphene
from graphene_django import DjangoObjectType
from .models import Aircraft, Airport, Arrival, Departure, Flight
from .service import getFlightsFromAirport, getFlightsToAirport
from django.db.models import Q, Count, Avg, Max, Min

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

class AirportStats(graphene.ObjectType):
    airport = graphene.String()
    total_airport_departures = graphene.Int()
    total_airport_arrivals = graphene.Int()
    avg_arrival_delay = graphene.Int()
    avg_departure_delay = graphene.Int()
    longest_arrival_delay = graphene.Int()
    longest_departure_delay = graphene.Int()

    def __str__(self):
        return f"{self.airport}, {self.total_airport_departures}, {self.total_airport_arrivals}, {self.avg_departure_delay}, {self.avg_arrival_delay}, {self.longest_departure_delay}, {self.longest_arrival_delay}"

class SAStatsType(graphene.ObjectType):
    total_departures = graphene.Int()
    total_arrivals = graphene.Int()
    total_num_airports = graphene.Int()
    highest_airport = graphene.String()
    lowest_airport = graphene.String()
    airport_stats = graphene.List(AirportStats)

def stats_resolver(parent, info):
    sa_airports = Airport.objects.filter(country='south africa')
    total_num_airports = sa_airports.count()
    total_departures = Departure.objects.all().count()
    total_arrivals = Arrival.objects.all().count()

    sa_aggregates = sa_airports.aggregate(Max('elevation'), Min('elevation'))
    highest_airport = sa_aggregates['elevation__max']*0.3048
    lowest_airport = sa_aggregates['elevation__min']*0.3048

    #Airport stats
    sa = sa_airports.annotate(Count('departure__airport'), Count('arrival__airport'), Avg('departure__time_delay'),Max('departure__time_delay'),Avg('arrival__time_delay'),Max('arrival__time_delay'))

    sa_airport_stats_list = []

    for airport in sa.values():
        x = AirportStats(
                airport = airport['name'],
                total_airport_departures = airport['departure__airport__count'], #incorrect result
                total_airport_arrivals = airport['arrival__airport__count'], #incorrect result
                avg_arrival_delay = airport['arrival__time_delay__avg'] ,
                avg_departure_delay = airport['departure__time_delay__avg'] ,
                longest_arrival_delay = airport['arrival__time_delay__max'] ,
                longest_departure_delay = airport['departure__time_delay__max'] ,
            )
        print(x)
        sa_airport_stats_list.append(x)
        

    return SAStatsType(
        total_departures = total_departures,
        total_arrivals = total_arrivals,
        total_num_airports = total_num_airports,
        highest_airport = highest_airport,
        lowest_airport = lowest_airport,
        airport_stats = sa_airport_stats_list,
    )
    
class Query(graphene.ObjectType):

    airports = graphene.List(AirportType, search=graphene.String())
    flights = graphene.List(FlightType, search=graphene.String())
    aircrafts = graphene.List(AircraftType, aircraft=graphene.String())
    stats = graphene.Field(SAStatsType, resolver=stats_resolver)

    def resolve_airports(root, info, search=None):
        if search:
            airport_query = Q(iata_code=search) | Q(icao_code__icontains=search) | Q(city__icontains=search) | Q(country__icontains=search) | Q(name__icontains=search)

            return Airport.objects.get(airport_query)
        else:
            return None
    
    def resolve_flights(root, info, search=None):

        x = {}

        if search:
            search_query = Q(number__icontains=search) | Q(iata_code__icontains=search) | Q(icao_code__icontains=search) | Q(status__icontains=search) | Q(airline__icontains=search)

            x = Flight.objects.filter(search_query)
            print(x.count())
        
            if x.count() == 0:

                airport_query = Q(iata_code=search) | Q(icao_code__icontains=search) | Q(city__icontains=search) | Q(country__icontains=search) | Q(name__icontains=search)

                airport = Airport.objects.get(airport_query)
                departures = Flight.objects.filter(departure__airport=airport)
                arrivals = Flight.objects.filter(arrival__airport=airport)

                y = departures | arrivals

                print(y.count())

                if y.count() < 50:

                    getFlightsFromAirport(airport.icao_code)
                    getFlightsToAirport(airport.icao_code)

                    return y
                else:
                    return y
            else:
                return x
        
        return None

schema = graphene.Schema(query=Query)