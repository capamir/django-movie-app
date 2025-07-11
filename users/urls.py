from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterViewSet, UserProfileViewSet, TokenObtainPairView, OTPVerificationViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/verify/', OTPVerificationViewSet.as_view({'post': 'create'}), name='otp_verify'),
]