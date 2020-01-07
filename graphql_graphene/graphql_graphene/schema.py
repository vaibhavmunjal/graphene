import graphene

from ingredients.graphql import schema as graphql_schema
class Query(graphql_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)