from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token

from .views import *


urlpatterns = [
    path("auth/", obtain_jwt_token),

]
