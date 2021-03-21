from api.logic.decorators import *


@check_access_to_request_account
def response_user_favorites(model_mixin, request, *args, **kwargs) -> Response:
    """
    Возвращает информацию об избранном пользователя
    """
    model_mixin.queryset = model_mixin.queryset.filter(user_id=kwargs.get('pk'))
    return model_mixin.list(request, *args, **kwargs)


def response_user_data_from_cookie(model_mixin, request, *args, **kwargs) -> Response:
    """
    Возвращает информацию о пользователе, полученной из токена в куки
    """
    serializer = model_mixin.get_serializer(request.user)

    return Response(serializer.data)


@check_access_to_request_account
def response_user_data(model_mixin, request, *args, **kwargs) -> Response:
    """
    Возвращает информацию о пользователе
    """
    serializer = model_mixin.get_serializer(model_mixin.queryset.objects.get(id=kwargs.get('pk')))
    return Response(serializer.data)

