import graphene
from graphene_django import DjangoObjectType
from .models import Aircraft, Airport, Flight
from .tasks import airportFlights
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
            'departure_airport',
            'departure_terminal',
            'departure_gate',
            'departure_baggage',
            'departure_time_delay',
            'departure_time_scheduled',
            'departure_time_actual',
            'arrival_airport',
            'arrival_terminal',
            'arrival_gate',
            'arrival_baggage',
            'arrival_time_delay',
            'arrival_time_scheduled',
            'arrival_time_actual',
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
    total_departures = 0
    total_arrivals = 0

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
    flights = graphene.List(FlightType, search=graphene.String(), searchone=graphene.String(), searchtwo=graphene.String())
    aircrafts = graphene.List(AircraftType, aircraft=graphene.String())
    stats = graphene.Field(SAStatsType, resolver=stats_resolver)
    flght = graphene.List(FlightType, search=graphene.String(), searchone=graphene.String(), searchtwo=graphene.String())

    def resolve_airports(root, info, search=None):
        if search:
            airport_query = Q(iata_code=search) | Q(icao_code__icontains=search) | Q(city__icontains=search) | Q(country__icontains=search) | Q(name__icontains=search)

            return Airport.objects.filter(airport_query)
        else:
            return Airport.objects.filter(country__icontains='south africa')

    def resolve_flights(root, info, search=None, searchone=None, searchtwo=None):

        departure_airport = ""
        arrival_airport = ""
        sa_airports = Airport.objects.filter(country="south africa")

        if search:
            search_query = Q(number__icontains=search) | Q(iata_code__icontains=search) | Q(icao_code__icontains=search) | Q(status__icontains=search) | Q(airline__icontains=search)
            airport_query = Q(iata_code__icontains=search) | Q(icao_code__icontains=search) | Q(city__icontains=search) | Q(country__icontains=search) | Q(name__icontains=search)
            flights = Flight.objects.filter(search_query)
            if flights.count() == 0:
                airports = sa_airports.filter(airport_query)
                flights = Flight.objects.filter(departure_airport__in=airports) | Flight.objects.filter(arrival_airport__in=airports)
                if flights.count() == 0 and airports.values().count() != 0:
                    airportFlights.delay(airports.values()[0]['icao_code'], "DEPARTURE")
                    airportFlights.delay(airports.values()[0]['icao_code'], "ARRIVAL")
            return flights
        elif searchone and searchtwo:
            airport_query = Q(iata_code=searchone) | Q(icao_code__icontains=searchone) | Q(city__icontains=searchone) | Q(country__icontains=searchone) | Q(name__icontains=searchone)
            arr_airport_query = Q(iata_code=searchtwo) | Q(icao_code__icontains=searchtwo) | Q(city__icontains=searchtwo) | Q(country__icontains=searchtwo) | Q(name__icontains=searchtwo)
            departure_airport = sa_airports.filter(airport_query)
            arrival_airport = sa_airports.filter(arr_airport_query)
            flights = Flight.objects.filter(departure_airport__in=departure_airport).filter(arrival_airport__in = arrival_airport).order_by("departure_time_scheduled")  
            return flights
        elif searchone:
            airport_query = Q(iata_code=searchone) | Q(icao_code__icontains=searchone) | Q(city__icontains=searchone) | Q(country__icontains=searchone) | Q(name__icontains=searchone)
            departure_airport = sa_airports.filter(airport_query)
            flights = Flight.objects.filter(departure_airport__in=departure_airport).order_by("departure_time_scheduled") 
            return flights
        elif searchtwo:
            arr_airport_query = Q(iata_code=searchtwo) | Q(icao_code__icontains=searchtwo) | Q(city__icontains=searchtwo) | Q(country__icontains=searchtwo) | Q(name__icontains=searchtwo)
            arrival_airport = sa_airports.filter(country="south africa")
            flights = Flight.objects.filter(arrival_airport__in=arrival_airport).order_by("arrival_time_scheduled")  
            return flights
        else:
            return None

schema = graphene.Schema(query=Query)