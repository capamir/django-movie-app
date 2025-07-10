from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_movies = models.ManyToManyField(Movie, related_name='favorited_by', blank=True)
    watched_movies = models.ManyToManyField(Movie, related_name='watched_by', blank=True)

    def __str__(self):
        return self.user.username

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP {self.code} for {self.phone_number}"