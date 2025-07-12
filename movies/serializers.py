from rest_framework import serializers
from .models import Genre, Actor, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source='genres'
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(), many=True, write_only=True, source='actors'
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'plot_summary', 'image', 'rating',
            'genres', 'actors', 'genre_ids', 'actor_ids', 'created_at'
        ]
        read_only_fields = ['created_at']
