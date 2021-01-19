from .rss import parse_anilibria_rss
from .models import *


def update_anime_data() -> None:
    """
    Поиск и обновление данных аниме с RSS канала Anilibria
    :return: None
    """
    anime_data = parse_anilibria_rss(
        last_title_date=AnimeDownloadLink.objects.all().order_by('-date_added')[0].date_added,
        filter_last=True
    )

    if anime_data:
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
