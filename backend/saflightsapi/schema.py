import graphene
from graphene_django import DjangoObjectType
from .models import Airport

class AirportType(DjangoObjectType):
    class Meta:
        model = Airport
        fields = (
            'iata_code',
            'airport_name',
            'municipality',
            'latitude_deg',
            'longitude_deg',
            'elevation',
            'image_url'
        )