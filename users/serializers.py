from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import UserProfile, OtpCode
from movies.models import Movie
from movies.serializers import MovieSerializer

class UserSerializerWithToken(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value
        return data

class OTPVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    phone = serializers.CharField(max_length=11)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializerWithToken(read_only=True)
    favorite_movies = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=True, required=False)
    watched_movies = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'favorite_movies', 'watched_movies']
        read_only_fields = ['user']

    def to_representation(self, instance):
        """Use nested serializers for read operations."""
        representation = super().to_representation(instance)
        representation['favorite_movies'] = MovieSerializer(instance.favorite_movies.all(), many=True).data
        representation['watched_movies'] = MovieSerializer(instance.watched_movies.all(), many=True).data
        return representation

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False  # Deactivate until OTP verification
        user.save()
        UserProfile.objects.create(user=user, phone_number=phone_number)
        return user