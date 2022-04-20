import graphene
import saflightsapi.schema

class Query(saflightsapi.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)