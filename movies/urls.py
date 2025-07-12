from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, ActorViewSet, MovieViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'actors', ActorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
