from api.logic.decorators import *


@check_access_to_request_account
def return_user_favorites(model_mixin, request, *args, **kwargs) -> Response:
    """
    Возвращает информацию об избранном пользователя
    """
    model_mixin.queryset = model_mixin.queryset.filter(user_id=kwargs.get('pk'))
    return model_mixin.list(request, *args, **kwargs)


@check_access_to_request_account
def return_user_data(model_mixin, request, *args, **kwargs) -> Response:
    """
    Возвращает информацию о пользователе
    """
    serializer = model_mixin.get_serializer(model_mixin.queryset.objects.get(id=kwargs.get('pk')))
    return Response(serializer.data)

