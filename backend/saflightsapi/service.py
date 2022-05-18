import requests
import datetime

from .models import Airport, Flight

key='8a8fafc5d36ed8340156288f3edb31eb'

def getFlightsFromAirport(airport_icao):
    departure_url = 'http://api.aviationstack.com/v1/flights?access_key='+key+'&dep_icao='+airport_icao
    departures_response = requests.get(departure_url)
    departures_json = departures_response.json()
    try:
        if departures_json.get('data'):
            print('if')
            saveData(departures_json)
        else:
            print('else')
            return None
    except Exception as e:
        pass

def getFlightsToAirport(airport_icao):
    
    arrival_url = 'http://api.aviationstack.com/v1/flights?access_key='+key+'&arr_icao='+airport_icao
    arrivals_response = requests.get(arrival_url)
    arrivals_json = arrivals_response.json()
    try:
        if arrivals_json.get('data'):
            print('if')
            saveData(arrivals_json)
        else:
            print('else')
            return None
    except Exception as s:
        pass

def saveData(flights):

    for flight in flights.get('data'):

        try:

            flght = Flight(
                iata_code = flight.get('flight').get('iata'),
                icao_code = flight.get('flight').get('icao'),
                number = flight.get('flight').get('number'),
                date = flight.get('flight_date'),
                status = flight.get('flight_status'),
                airline = flight.get('airline').get('name'),
                departure_airport = Airport.objects.get(icao_code=flight.get('departure').get('icao')),
                departure_terminal = flight.get('departure').get('terminal'),
                departure_gate = flight.get('departure').get('gate'),
                departure_time_delay = flight.get('departure').get('delay'),
                departure_time_scheduled = formatDate(flight.get('departure').get('scheduled')),
                departure_time_actual = formatDate(flight.get('departure').get('actual')),
                arrival_airport = Airport.objects.get(icao_code=flight.get('arrival').get('icao')),
                arrival_terminal = flight.get('arrival').get('terminal'),
                arrival_gate = flight.get('arrival').get('gate'),
                arrival_time_delay = flight.get('arrival').get('delay'),
                arrival_time_scheduled = formatDate(flight.get('arrival').get('scheduled')),
                arrival_time_actual = formatDate(flight.get('arrival').get('actual')),
            )
            flght.save()

        except Exception as er:
            print (f"{er}, {flight.get('departure').get('icao')} -> {flight.get('arrival').get('icao')}")

def formatDate(date_string): 
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    if(date_string == 'None' or date_string is None or date_string == '' or date_string == 'null' ):
        return None
    else:
        utc_date = datetime.datetime.strptime(date_string ,date_format)
        return utc_date + datetime.timedelta(hours=2)