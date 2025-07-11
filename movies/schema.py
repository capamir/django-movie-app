import graphene
from graphene_django import DjangoObjectType
from .models import Movie, Genre, Actor
from movies.permissions import IsAdminOrReadOnly
from graphene_django.filter import DjangoFilterConnectionField

# GraphQL Types
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'plot_summary', 'image', 'rating', 'genres', 'actors', 'created_at']
        filter_fields = {
            'title': ['exact', 'icontains'],
            'genres__name': ['exact'],
            'actors__name': ['exact'],
            'rating': ['gte', 'lte']
        }
        interfaces = (graphene.relay.Node,)

class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        filter_fields = {'name': ['exact', 'icontains']}
        interfaces = (graphene.relay.Node,)

class ActorType(DjangoObjectType):
    class Meta:
        model = Actor
        fields = ['id', 'name']
        filter_fields = {'name': ['exact', 'icontains']}
        interfaces = (graphene.relay.Node,)

# Query Class
class MovieQuery(graphene.ObjectType):
    all_movies = DjangoFilterConnectionField(MovieType)
    all_genres = DjangoFilterConnectionField(GenreType)
    all_actors = DjangoFilterConnectionField(ActorType)
    movie = graphene.Field(MovieType, id=graphene.Int())
    genre = graphene.Field(GenreType, id=graphene.Int())
    actor = graphene.Field(ActorType, id=graphene.Int())

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_all_genres(self, info):
        return Genre.objects.all()

    def resolve_all_actors(self, info):
        return Actor.objects.all()

    def resolve_movie(self, info, id):
        return Movie.objects.get(pk=id)

    def resolve_genre(self, info, id):
        return Genre.objects.get(pk=id)

    def resolve_actor(self, info, id):
        return Actor.objects.get(pk=id)

# Mutation Class
class CreateMovie(graphene.Mutation):
    movie = graphene.Field(MovieType)

    class Arguments:
        title = graphene.String(required=True)
        plot_summary = graphene.String(required=True)
        rating = graphene.Float(required=True)
        genre_ids = graphene.List(graphene.Int, required=True)
        actor_ids = graphene.List(graphene.Int, required=True)

    def mutate(self, info, title, plot_summary, rating, genre_ids, actor_ids):
        if not IsAdminOrReadOnly().has_permission(info.context, None):
            raise Exception("Admin access required")
        movie = Movie.objects.create(title=title, plot_summary=plot_summary, rating=rating)
        movie.genres.set(Genre.objects.filter(id__in=genre_ids))
        movie.actors.set(Actor.objects.filter(id__in=actor_ids))
        movie.save()
        return CreateMovie(movie=movie)

class CreateGenre(graphene.Mutation):
    genre = graphene.Field(GenreType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        if not IsAdminOrReadOnly().has_permission(info.context, None):
            raise Exception("Admin access required")
        genre = Genre.objects.create(name=name)
        return CreateGenre(genre=genre)

class CreateActor(graphene.Mutation):
    actor = graphene.Field(ActorType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        if not IsAdminOrReadOnly().has_permission(info.context, None):
            raise Exception("Admin access required")
        actor = Actor.objects.create(name=name)
        return CreateActor(actor=actor)

class MovieMutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    create_genre = CreateGenre.Field()
    create_actor = CreateActor.Field()