from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .logic import *
from .serializers import *
from watcher import models


class UserFavoriteListView(ListAPIView):
    """
    Контроллер, отвечающий за взаимодействие с моделью UserFavorite
    """
    serializer_class = UserFavoriteSerializer
    queryset = models.UserFavorite.objects
    permission_classes = (IsAuthenticated,)

    # GET запрос на получение данные об избранном пользователя
    def get(self, request, *args, **kwargs):
        return return_user_favorites(self, request, *args, **kwargs)


class UserDataView(RetrieveAPIView):
    """
    Контроллер, отвечающий за взаимодействие с моделью User
    """
    serializer_class = UserSerializer
    queryset = models.User
    permission_classes = (AllowAny,)

    # GET запрос на получение данные о пользователе
    def get(self, request, *args, **kwargs):
        return return_user_data(self, request, *args, **kwargs)

