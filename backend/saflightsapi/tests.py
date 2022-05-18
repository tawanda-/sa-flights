import json
from django.test import TestCase
from .models import Airport
from graphene_django.utils.testing import GraphQLTestCase

class SAFlightsApiTestCase(GraphQLTestCase):

    fixtures = ["test_airports_fixture.json", "test_flights_fixture.json"]
    GRAPHQL_URL = '/graphql'

    def test_airport_query(self):
        response = self.query('''query Airports($search: String) {airports(search: $search){ name iataCode icaoCode imageUrl}}''',variables={'search': 'fact'})
        content = json.loads(response.content)
        self.assertEqual(content, {'data':{'airports':[{'name':'Cape Town International Airport','iataCode':'CPT', 'icaoCode':'FACT','imageUrl':'https://thumbs2.imgbox.com/6b/65/hln93WAv_t.jpeg'}]}}, 'Response has correct data')

    
    def test_flight_search_query(self):
        response = self.query(
            '''
            query Flights($search: String){
                flights(search: $search){
                    number
                    iataCode
                    icaoCode
                    date
                    status
                    airline
                    arrivalGate
                    arrivalBaggage
                    arrivalTerminal
                    arrivalTimeDelay
                    arrivalTimeScheduled
                    departureGate
                    departureBaggage
                    departureTerminal
                    departureTimeDelay
                    departureTimeScheduled
                    departureAirport{
                        name
                        icaoCode
                        iataCode
                        latitudeDeg
                        elevation
                        imageUrl
                    }
                    arrivalAirport{
                        name
                        icaoCode
                        iataCode
                        latitudeDeg
                        elevation
                        imageUrl
                    }
                }
                arrivalAirport{
                    name
                    icaoCode
                    iataCode
                    latitudeDeg
                    elevation
                    imageUrl
                }
                }}
            ''',
            variables={'search': 'FABL'}
        )
        content = json.loads(response.content)
        self.assertEqual(content.get('data'), {'flights': .get({'number': '600', 'iataCode': '4Z600', 'icaoCode': 'LNK600', 'date': '2022-04-29', 'status': 'landed', 'airline': 'South African Airlink', 'arrivalGate': None, 'arrivalBaggage': None, 'arrivalTerminal': 'B', 'arrivalTimeDelay': None, 'arrivalTimeScheduled': '09:35:00', 'departureGate': 'A10', 'departureBaggage': None, 'departureTerminal': None, 'departureTimeDelay': 14, 'departureTimeScheduled': '08:00:00', 'departureAirport': {'name': 'Cape Town International Airport', 'icaoCode': 'FACT', 'iataCode': 'CPT', 'latitudeDeg': -33.96480179, 'elevation': 151, 'imageUrl': 'https://thumbs2.imgbox.com/6b/65/hln93WAv_t.jpeg'}, 'arrivalAirport': {'name': 'Bram Fischer International Airport', 'icaoCode': 'FABL', 'iataCode': 'BFN', 'latitudeDeg': -29.092699, 'elevation': 4457, 'imageUrl': 'https://thumbs2.imgbox.com/33/1a/4TcUIR16_t.jpeg'}})}, 'Response has correct data')
