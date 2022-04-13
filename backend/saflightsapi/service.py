import json
import requests
from datetime import datetime

from .models import Airport, Flight, FlightDetail

def getFlights():

    url = 'http://api.aviationstack.com/v1/flights?access_key=22e42fab53f8273bf7ee4d10c1945238'
    response = requests.get(url)
    flights = response.json()

    saveData(flights=flights)

def getAirportFlights(code):
    dep_url = 'http://api.aviationstack.com/v1/flights?access_key=22e42fab53f8273bf7ee4d10c1945238&dep_iata='+code
    arr_url = 'http://api.aviationstack.com/v1/flights?access_key=22e42fab53f8273bf7ee4d10c1945238&arr_iata='+code
    
    dep_response = requests.get(dep_url)
    arr_response = requests.get(arr_url)
    
    dep_flights = dep_response.json()
    arr_flights = arr_response.json()

    saveData(dep_flights)
    saveData(arr_flights)

def saveData(flights):

    for flight in flights['data']:

        x = "{}, {} flight #{}, departs {} at {} & arrives {} at {} {} -> {}"
        print(x.format(flight['flight_status'],flight['airline']['name'],flight['flight']['number'],flight['departure']['airport'],flight['departure']['scheduled'],flight['arrival']['airport'],flight['arrival']['scheduled'],flight['departure']['icao'], flight['arrival']['icao']))

        dep = FlightDetail(
            status = 'DEPARTURE',
            terminal = flight['departure']['terminal'],
            gate = flight['departure']['gate'],
            baggage = '',
            time_delay = flight['departure']['delay'],
            time_scheduled = formatDate(flight['departure']['scheduled']),
            time_estimated = formatDate(flight['departure']['estimated']),
            time_actual = formatDate(flight['departure']['actual']),
            estimated_runway = formatDate(flight['departure']['estimated_runway']),
            actual_runway = formatDate(flight['departure']['actual_runway']),
        )
        
        arr = FlightDetail(
            status = 'ARRIVAL',
            terminal = flight['arrival']['terminal'],
            gate = flight['arrival']['gate'],
            baggage = '',
            time_delay = flight['arrival']['delay'],
            time_scheduled = formatDate(flight['arrival']['scheduled']),
            time_estimated = formatDate(flight['arrival']['estimated']),
            time_actual = formatDate(flight['arrival']['actual']),
            estimated_runway = formatDate(flight['arrival']['estimated_runway']),
            actual_runway = formatDate(flight['arrival']['actual_runway']),
        )
        flght = Flight(
            iata_code = flight['flight']['iata'],
            icao_code = flight['flight']['icao'],
            number = flight['flight']['number'],
            date = flight['flight_date'],
            status = flight['flight_status'],
            airline = flight['airline']['name'],
            )

        try:
            source = Airport.objects.get(icao_code=flight['arrival']['icao'])
            destination = Airport.objects.get(icao_code=flight['departure']['icao'])

            dep.save()
            arr.save()

            flght.departure = dep
            flght.arrival = arr
            flght.destination_airport = source
            flght.source_airport = destination

            flght.save()

        except:
            print('## Skipped airport not found')


def formatDate(date_string): 
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    if(date_string == 'None' or date_string is None or date_string is '' or date_string == 'null' ):
        return None
    else:
        return datetime.strptime(date_string ,date_format)