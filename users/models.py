from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class UserProfile(models.Model):
    """User profile with phone number and movie preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Associated user account")
    phone_number = models.CharField(max_length=11, blank=True, null=True, help_text="User's phone number for OTP")
    favorite_movies = models.ManyToManyField(Movie, related_name='favorited_by', blank=True, help_text="User's favorite movies")
    watched_movies = models.ManyToManyField(Movie, related_name='watched_by', blank=True, help_text="Movies the user has watched")

    def __str__(self):
        return self.user.username

class OtpCode(models.Model):
    """Temporary OTP code for user verification."""
    phone_number = models.CharField(max_length=11, help_text="Phone number for OTP")
    code = models.IntegerField(help_text="4-digit OTP code")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")

    def __str__(self):
        return f"OTP {self.code} for {self.phone_number}"