from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_403_FORBIDDEN

from watcher import models as watcher_models


def check_access_to_request_account(func):
    """
    Декоратор, проверяющий, имеет ли клиент доступ
    к запрашиваемой информации об аккаунте
    """
    def wrapper(*args, **kwargs):
        """
        Условие сравниет запрашиваемого пользователя и аккаунт, с которого пришел запрос,
        если они одинаковые, то отдает инфу, если нет, то ответ 403
        Конструкция в правой части нужна, чтобы найти, где в *args объект с классом, так как неочевидно,
        как могу быть переданны аргументы
        """
        if watcher_models.User.objects.get(id=kwargs.get('pk')) == [x for x in args if isinstance(x, Request)][0].user:
            return func(*args, **kwargs)
        else:
            return Response(data={"message": "Permission error"}, status=HTTP_403_FORBIDDEN)

    return wrapper
