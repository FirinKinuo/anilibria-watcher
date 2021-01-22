from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token

from .views import *


urlpatterns = [
    path("auth/", obtain_jwt_token),
    path("anime/", AllAnimeView.as_view()),
    path("anime/<int:pk>", AnimeView.as_view())
]
