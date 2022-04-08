from re import A
from typing_extensions import Required
import graphene
from graphene_django import DjangoObjectType
from .models import Airport

class AirportType(DjangoObjectType):
    class Meta:
        model = Airport
        fields = (
            'iata_code',
            'name',
            'municipality',
            'latitude_deg',
            'longitude_deg',
            'elevation',
            'image_url'
        )

class Query(graphene.ObjectType):

    airports = graphene.List(AirportType)
    airport = graphene.Field(AirportType, iata_code=graphene.String(required=True))
        
    def resolve_airports(root, info):
        return Airport.objects.all()

    def resolve_airport(root, info, iata_code):
        try:
            return Airport.objects.get(iata_code=iata_code)
        except Airport.DoesNotExist:
            return None
    
schema = graphene.Schema(query=Query)