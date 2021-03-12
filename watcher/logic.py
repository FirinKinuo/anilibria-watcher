from .api_requests import *
from .models import *
from webhooks import send_webhook


def add_anime_data(anime_data: list) -> None:
    """
    Обновление таблицы Anime
    :param anime_data: Список с словарем данных
    :return: None
    """

    for anime in anime_data:
        Anime.objects.update_or_create(
            anilibria_id=anime["id"],
            defaults={
                "anilibria_id": anime["id"],
                "original_name": anime["names"]["en"],
                "updated_at": anime["updated"] if anime['updated'] is not None else anime['last_change']
                })


def get_anime_data_from_api(arg_last_anime=0, arg_limit=5) -> list:
    """
    Возвращает список с обновлениями по тайтлам
    :param int arg_last_anime: unix-time последнего тайтла
    :param int arg_limit: кол-во выдачи тайтлов
    :return list: Список с обновленными тайтлами
    """
    try:
        return get_updates(
            # +1 к updated_at, чтобы отсечь последний тайтл
            last_anime_date=Anime.objects.latest('updated_at').updated_at+1 if arg_last_anime == 0 else arg_last_anime,
            limit=arg_limit
        )
    except Anime.DoesNotExist:
        # Если БД пустая(обычно при первом запуске), то отправить запрос без фильтрации по последнему тайтлу
        return get_updates()


def user_anime_filter(user: User, anime_data: list) -> list:
    """
    Возвращает список с отфильтрованными по избранному пользователя
    :param user: Модель User
    :param anime_data: Список с данными
    :return: Отфильтрованный список с данными
    """
    favorites = UserFavorite.objects.filter(user=user.id)
    if not favorites:
        return anime_data

    return [anime for anime in anime_data for fav in favorites if anime['anilibria_id'] == fav.anime.anilibria_id]


def send_webhooks_to_users(anime_data: list) -> None:
    """
    Отправляет вебхуки пользователям по их спискам избранного
    :param anime_data: Список с данными
    :return: None
    """

    users = User.objects.all()

    for user in users:
        data_to_send = user_anime_filter(user=user, anime_data=anime_data)
        send_webhook(user.webhooks_urls, content=data_to_send)
