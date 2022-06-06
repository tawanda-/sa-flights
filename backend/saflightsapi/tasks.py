import json
import requests
from django.conf import settings 
from django.db import transaction
from .models import Airport, Flight
from celery import shared_task

key=settings.AIRLABS_KEY

@shared_task
def airportFlights(airport_icao, movement):
    url = ''
    if movement == "DEPARTURE":
        url = "https://airlabs.co/api/v9/schedules?dep_icao="+airport_icao+"&api_key="+settings.AIRLABS_KEY
    elif movement == "ARRIVAL":
        url = "https://airlabs.co/api/v9/schedules?arr_icao="+airport_icao+"&api_key="+settings.AIRLABS_KEY
    else:
        return
    
    response = requests.get(url)
    response_json = response.json()
    saveResponse(response_json.get('response'))

def getCountry(iso2):
    url = 'http://api.worldbank.org/v2/country/'+iso2+'?format=json'
    response = requests.get(url)
    response_json = response.json()

    if response_json[1][0]["name"]:
        return response_json[1][0]["name"]
    else:
        return ""

@shared_task
def saveAirport(icao):

    if icao:
        url = 'https://airlabs.co/api/v9/airports?icao_code='+icao+'&api_key=93476355-01d5-44fd-848b-4a75cb43f051'
        response = requests.get(url)
        airport = response.json()['response'][0]
        
        try:
            with transaction.atomic():
                Airport(
                    name = airport.get("name"),
                    iata_code=airport.get("iata_code"),
                    icao_code=airport.get("icao_code"),
                    latitude_deg=airport.get("lat"),
                    longitude_deg=airport.get("lng"),
                    elevation=airport.get("alt"),
                    country = "",
                    city=airport.get("city"),
                ).save()
        except:
            return
    else:
        return


def saveResponse(flights):

    insert_list = []

    for flight in flights:

        dep = None
        arr = None
        try:
            dep = Airport.objects.get(icao_code=flight.get('dep_icao'))
        except:
            print(f"get airport {flight.get('dep_icao')}")
            saveAirport(flight.get('dep_icao'))
            continue
            
        try:
            arr = Airport.objects.get(icao_code=flight.get('arr_icao'))
        except:
            print(f"get airport {flight.get('arr_icao')}")
            saveAirport(flight.get('arr_icao'))
            continue
        
        try:
            flight_ = Flight(
                iata_code = flight.get('flight_iata'),
                icao_code = flight.get('flight_icao'),
                number = flight.get('flight_number'),
                date = flight.get('dep_time').split()[0],
                status = flight.get('status'),
                airline = flight.get('airline_icao'),

                departure_airport = dep,
                departure_terminal = flight.get('dep_terminal'),
                departure_gate = flight.get('dep_gate'),
                departure_time_scheduled = flight.get('dep_time').split()[1],
                departure_time_actual = flight.get('arr_time').split()[1] if not flight.get('dep_estimated') else flight.get('dep_estimated').split()[1],

                arrival_airport = arr,
                arrival_terminal = flight.get('arr_terminal'),
                arrival_gate = flight.get('arr_gate'),
                arrival_time_scheduled = flight.get('arr_time').split()[1],
                arrival_time_actual = flight.get('arr_time').split()[1] if not flight.get('arr_estimated') else flight.get('arr_estimated').split()[1],
            )
            insert_list.append(flight_)
        except:
            print(flight.get('flight_iata'))

    try:
        Flight.objects.bulk_create(insert_list)
    except:
        return