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
    favorite_movies = MovieSerializer(many=True)
    watched_movies = MovieSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'favorite_movies', 'watched_movies']

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
        # TODO: Generate and send OTP code here (e.g., via SMS or email)
        # For now, assume OTP is manually created in OtpCode model
        return user