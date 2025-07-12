from django.contrib import admin
from .models import Movie, Genre, Actor



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for Movie model."""
    list_display = ('title', 'rating', 'created_at',)
    list_filter = ('rating', 'created_at', 'genres', 'actors')
    search_fields = ('title', 'plot_summary')
    date_hierarchy = 'created_at'
    list_per_page = 20


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin interface for Genre model."""
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_per_page = 20

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Admin interface for Actor model."""
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20