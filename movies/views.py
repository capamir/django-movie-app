from rest_framework import viewsets
from .models import Movie, Genre, Actor
from .serializers import MovieSerializer, GenreSerializer, ActorSerializer
from .permissions import IsAdminOrReadOnly

class MovieViewSet(viewsets.ModelViewSet):
    """Manage movies: list, create, retrieve, update, delete."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

class GenreViewSet(viewsets.ModelViewSet):
    """Manage genres: list, create, retrieve, update, delete."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class ActorViewSet(viewsets.ModelViewSet):
    """Manage actors: list, create, retrieve, update, delete."""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]