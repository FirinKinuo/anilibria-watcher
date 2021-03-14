from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from .views import *


urlpatterns = [
    path("auth/", obtain_jwt_token),
    path("auth/verify/", verify_jwt_token),
    path("user/<int:pk>/", UserDataView.as_view()),
    path("user/<int:pk>/favorites/", UserFavoriteListView.as_view())
]
