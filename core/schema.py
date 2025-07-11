import graphene
from movies.schema import MovieQuery, MovieMutation

class Query(MovieQuery, graphene.ObjectType):
    pass

class Mutation(MovieMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)