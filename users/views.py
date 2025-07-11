from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile, OtpCode
from .serializers import (
    UserProfileSerializer, RegisterSerializer,
    TokenObtainPairSerializer, OTPVerificationSerializer
)
from movies.permissions import IsAdminOrReadOnly

class TokenObtainPairView(BaseTokenObtainPairView):
    """Obtain JWT access and refresh tokens with user data."""
    serializer_class = TokenObtainPairSerializer

class OTPVerificationViewSet(CreateModelMixin, GenericViewSet):
    """Verify OTP code to activate user account."""
    queryset = OtpCode.objects.all()
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]  # Public access for OTP verification

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone')
            otp_code = int(serializer.validated_data.get('code'))
            
            try:
                otp_obj = OtpCode.objects.get(phone_number=phone_number)
                saved_otp_code = otp_obj.code
            except OtpCode.DoesNotExist:
                return Response({'message': 'OTP code not found for the provided phone number'}, status=status.HTTP_404_NOT_FOUND)
            
            if otp_code == saved_otp_code:
                try:
                    profile = UserProfile.objects.get(phone_number=phone_number)
                    user = profile.user
                    user.is_active = True
                    user.save()
                    otp_obj.delete()
                    return Response({'message': 'OTP code verified successfully'}, status=status.HTTP_200_OK)
                except UserProfile.DoesNotExist:
                    return Response({'message': 'User not found for this phone number'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterViewSet(viewsets.ModelViewSet):
    """Register a new user with username, email, password, and phone number."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow public registration
    http_method_names = ['post']  # Only allow POST for registration

class UserProfileViewSet(viewsets.ModelViewSet):
    """Manage user profiles: view or update favorite/watched movies."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Restrict to the current user's profile unless admin."""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Handle custom actions for adding/removing favorite/watched movies."""
        instance = serializer.instance
        action = self.request.data.get('action')
        movie_id = self.request.data.get('movie_id')

        if action == 'add_favorite':
            instance.favorite_movies.add(movie_id)
        elif action == 'remove_favorite':
            instance.favorite_movies.remove(movie_id)
        elif action == 'add_watched':
            instance.watched_movies.add(movie_id)
        elif action == 'remove_watched':
            instance.watched_movies.remove(movie_id)
        serializer.save()