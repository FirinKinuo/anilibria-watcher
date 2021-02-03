from .rss import parse_anilibria_rss
from .models import *
from webhooks import send_webhook


def update_anime_models(anime_data: list) -> None:
    """
    Обновление моделей Anime и AnimeDownloadLink
    :param anime_data: Словарь с данными
    :return: None
    """
    for anime in anime_data:
        Anime.objects.update_or_create(darklibria_link=anime["darklibria_link"], defaults={
            "name": anime["name"],
            "original_name": anime["original_name"],
            "description": anime["description"],
            "episode_count": anime["episode_count"],
            "current_episode": anime["current_episode"],
            "darklibria_link": anime["darklibria_link"],
        })

        try:
            AnimeDownloadLink.objects.update_or_create(
                id=AnimeDownloadLink.objects.filter(
                    anime_id=Anime.objects.get(darklibria_link=anime["darklibria_link"]).id,
                    type=anime["download_link"]["type"]).get().id,
                defaults={
                    "anime_id": Anime.objects.get(darklibria_link=anime["darklibria_link"]).id,
                    "type": anime["download_link"]["type"],
                    "link": anime["download_link"]["link"],
                    "date_added": anime["download_link"]["date_added"]
                })
        except AnimeDownloadLink.DoesNotExist:
            AnimeDownloadLink.objects.create(
                anime_id=Anime.objects.get(darklibria_link=anime["darklibria_link"]).id,
                type=anime["download_link"]["type"],
                link=anime["download_link"]["link"],
                date_added=anime["download_link"]["date_added"],
            )


def get_anime_data() -> [list, None]:
    """
    Возвращает None или список с последними данными по аниме из RSS канала
    :return: Возвращает list, если получены данные, иначе None
    """
    try:
        return parse_anilibria_rss(
            last_title_link=AnimeDownloadLink.objects.latest("link").link,
            filter_last=True
        )

    except AnimeDownloadLink.DoesNotExist:
        return parse_anilibria_rss()


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

    return [anime for anime in anime_data for fav in favorites if anime['darklibria_link'] == fav.anime.darklibria_link]


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
