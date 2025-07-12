from django.contrib import admin
from .models import Movie, Genre, Actor

class GenreInline(admin.TabularInline):
    """Inline admin for genres in Movie admin."""
    model = Movie.genres.through
    extra = 1
    verbose_name = "Genre"
    verbose_name_plural = "Genres"

class ActorInline(admin.TabularInline):
    """Inline admin for actors in Movie admin."""
    model = Movie.actors.through
    extra = 1
    verbose_name = "Actor"
    verbose_name_plural = "Actors"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for Movie model."""
    list_display = ('title', 'rating', 'created_at', 'genre_list', 'actor_list')
    list_filter = ('rating', 'created_at', 'genres', 'actors')
    search_fields = ('title', 'plot_summary')
    inlines = [GenreInline, ActorInline]
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