from django.urls import path
from .views import MovieListCreateView, MovieDetailView, GenreListView, ActorListView

urlpatterns = [
    path('', MovieListCreateView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('actors/', ActorListView.as_view(), name='actor-list'),
]