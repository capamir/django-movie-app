from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    plot_summary = models.TextField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    rating = models.FloatField(default=0.0, choices=[(i * 0.5, str(i * 0.5)) for i in range(11)])
    genres = models.ManyToManyField(Genre, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title