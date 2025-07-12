from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from graphene_django.views import GraphQLView

schema_view = get_schema_view(
    openapi.Info(
        title="Movie API",
        default_version='v1',
        description="API for managing movies, genres, actors, and user profiles with JWT and OTP authentication",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/movies/', include('movies.urls')),
    path('api/users/', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('graphql/', GraphQLView.as_view(graphiql=True), name='graphql'),  # GraphQL endpoint with GraphiQL
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)