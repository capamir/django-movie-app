from django.db import models

class Genre(models.Model):
    """A category for classifying movies (e.g., Action, Drama)."""
    name = models.CharField(max_length=100, help_text="Name of the genre")

    def __str__(self):
        return self.name

class Actor(models.Model):
    """An actor appearing in movies."""
    name = models.CharField(max_length=100, help_text="Name of the actor")

    def __str__(self):
        return self.name

class Movie(models.Model):
    """A movie with details like title, plot, and rating."""
    title = models.CharField(max_length=200, help_text="Title of the movie")
    plot_summary = models.TextField(help_text="Summary of the movie's plot")
    image = models.ImageField(upload_to='movies/', blank=True, null=True, help_text="Poster image of the movie")
    rating = models.FloatField(default=0.0, choices=[(i * 0.5, str(i * 0.5)) for i in range(11)], help_text="Rating out of 5")
    genres = models.ManyToManyField(Genre, related_name='movies', help_text="Genres associated with the movie")
    actors = models.ManyToManyField(Actor, related_name='movies', help_text="Actors in the movie")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")

    def __str__(self):
        return self.title