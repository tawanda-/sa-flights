import json
from django.test import TestCase
from .models import Airport
from graphene_django.utils.testing import GraphQLTestCase

class SAFlightsApiTestCase(GraphQLTestCase):

    def setUp(self):
        Airport.objects.create(
            iata_code ='MQP', 
            name ='Kruger Mpumalanga International Airport', 
            municipality ='Mpumalanga',
            latitude_deg = '-25.38319969',
            longitude_deg =	'31.10560036',
            elevation = '2829',
            image_url = "https://imgbox.com/rC5HhVTD"
        )
        

    def test_airports_query(self):
        response = self.query(
            '''
            query {
                airports{
                    name,municipality,iataCode,latitudeDeg,longitudeDeg,elevation,imageUrl
                }
            }
            ''',
            op_name = 'airports'
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_airport_query(self):
        response = self.query(
            '''
            query {
                airport{
                    name,municipality,iataCode,latitudeDeg,longitudeDeg,elevation,imageUrl
                }
            }
            ''',
            op_name='airport',
            variables={'iataCode': 'MQP'}
        )

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)