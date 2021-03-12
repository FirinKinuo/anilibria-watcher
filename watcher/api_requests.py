from requests import get as req_get

HOST_URL = "https://api.anilibria.tv/v2/"


def get_updates(last_anime_date=0, limit=5) -> list:
    """
    Получить краткий список данных с 5 последними обновленными тайтлами,
    либо отфильтрованным до последнего по last_anime_date
    :param int last_anime_date: id последнего тайтла
    :param int limit: кол-во выдачи тайтлов
    :return: list с id, names.en, updated
    """

    response_data = req_get(
        url=f"{HOST_URL}getUpdates",
        params={
            "filter": "id,names.en,updated,last_change",
            "since": last_anime_date,
            "limit": limit
        }).json()

    return response_data

