import requests
import datetime

from .models import Airport, Flight, Departure, Arrival

def getFlightsFromAirport(airport_icao):
    departure_url = 'http://api.aviationstack.com/v1/flights?access_key=a46c18b7dcab20f45efb6e592b5fa9c1&dep_icao='+airport_icao
    departures_response = requests.get(departure_url)
    departures_json = departures_response.json()
    saveData(departures_json)

def getFlightsToAirport(airport_icao):
    
    arrival_url = 'http://api.aviationstack.com/v1/flights?access_key=a46c18b7dcab20f45efb6e592b5fa9c1&arr_icao='+airport_icao
    arrivals_response = requests.get(arrival_url)
    arrivals_json = arrivals_response.json()
    saveData(arrivals_json)

def saveData(flights):

    for flight in flights['data']:

        try:

            dep = Departure(
                airport = Airport.objects.get(icao_code=flight['departure']['icao']),
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
        
            arr = Arrival(
                airport = Airport.objects.get(icao_code=flight['arrival']['icao']),
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
            
            dep.save()
            arr.save()

            flght.departure = dep
            flght.arrival = arr
            flght.save()

        except Exception as er:
            print (er)

def formatDate(date_string): 
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    if(date_string == 'None' or date_string is None or date_string == '' or date_string == 'null' ):
        return None
    else:
        utc_date = datetime.datetime.strptime(date_string ,date_format)
        return utc_date + datetime.timedelta(hours=2)