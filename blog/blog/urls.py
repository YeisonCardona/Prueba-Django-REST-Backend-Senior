"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view

# schema_view = get_schema_view(
    # openapi.Info(
        # title="Tu API",
        # default_version='v1',
        # description="Descripción de tu API",
    # ),
    # public=True,
# )

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from posts import views as posts_views
from users import views as users_views

router = routers.DefaultRouter()
router.register(r'users', users_views.UserViewSet, basename='user')
router.register(r'profiles', users_views.ProfileViewSet, basename='profile')
router.register(r'posts', posts_views.PostViewSet, basename='post')
router.register(r'tags', posts_views.TagViewSet, basename='tag')
router.register(r'comments', posts_views.CommentViewSet, basename='comment')
router.register(r'likes', posts_views.LikeViewSet, basename='like')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
