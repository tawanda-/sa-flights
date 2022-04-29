import requests
import datetime

from .models import Airport, Flight

def getFlightsFromAirport(airport_icao):
    departure_url = 'http://api.aviationstack.com/v1/flights?access_key=55e7fe11184e868b4c9464df13555e72&dep_icao='+airport_icao
    departures_response = requests.get(departure_url)
    departures_json = departures_response.json()
    saveData(departures_json)

def getFlightsToAirport(airport_icao):
    
    arrival_url = 'http://api.aviationstack.com/v1/flights?access_key=55e7fe11184e868b4c9464df13555e72&arr_icao='+airport_icao
    arrivals_response = requests.get(arrival_url)
    arrivals_json = arrivals_response.json()
    saveData(arrivals_json)

def saveData(flights):

    for flight in flights['data']:

        try:

            flght = Flight(
                iata_code = flight['flight']['iata'],
                icao_code = flight['flight']['icao'],
                number = flight['flight']['number'],
                date = flight['flight_date'],
                status = flight['flight_status'],
                airline = flight['airline']['name'],
                departure_airport = Airport.objects.get(icao_code=flight['departure']['icao']),
                departure_terminal = flight['departure']['terminal'],
                departure_gate = flight['departure']['gate'],
                departure_time_delay = flight['departure']['delay'],
                departure_time_scheduled = formatDate(flight['departure']['scheduled']),
                departure_time_actual = formatDate(flight['departure']['actual']),
                arrival_airport = Airport.objects.get(icao_code=flight['arrival']['icao']),
                arrival_terminal = flight['arrival']['terminal'],
                arrival_gate = flight['arrival']['gate'],
                arrival_time_delay = flight['arrival']['delay'],
                arrival_time_scheduled = formatDate(flight['arrival']['scheduled']),
                arrival_time_actual = formatDate(flight['arrival']['actual']),
            )
            print(flght)
            flght.save()

        except Exception as er:
            print (f"{er}, {flight['departure']['icao']} -> {flight['arrival']['icao']}")

def formatDate(date_string): 
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    if(date_string == 'None' or date_string is None or date_string == '' or date_string == 'null' ):
        return None
    else:
        utc_date = datetime.datetime.strptime(date_string ,date_format)
        return utc_date + datetime.timedelta(hours=2)