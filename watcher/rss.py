import feedparser


def _find_current_episode(dirty_str: str) -> int:
    """
    Поиск текущего эпизода
    :param dirty_str: Грязная строка с лишними данными, из которой надо вытянуть число
    :return: Возвращает int с текущей серией
    """

    try:
        return int(dirty_str.split('-')[1][:dirty_str.split('-')[1].find(" ")])
    except IndexError:
        # Если в тайтле вышла первая серия, то поиск разделением не получится
        return int(dirty_str[dirty_str.find(":")+1:dirty_str.find("[")].replace(" ", ""))


def _filter_last_anime(rss: list, last_title_link: str) -> list:
    """
    Возращает отфильтрованный до последнего тайтла в записи список аниме
    :param rss: Список RSS для фильтрации
    :param last_title_link: Ссылка на скачивание последнего тайтла
    :return: Отфильтрованный список RSS
    """

    for i, el in enumerate(rss):
        if el.links[-1].href == last_title_link:
            return rss[:i]
    return rss


def parse_anilibria_rss(last_title_link=None, filter_last=False) -> (list, None):
    """
    Получить готовый список с данными по последним 30 тайтлам в списке

    :param last_title_link: Ссылка на скачивание последнего тайтла для проверки на обновление списка
    :param filter_last: Проводить ли фильтрацию до последнего записанного тайтла, необходим last_title_date
    :return: Возвращает список последних в RSS тайтлов, либо None, если нет новых тайтлов
    """

    rss = feedparser.parse("https://dark-libria.it/rss.xml").entries

    if last_title_link is not None:

        if last_title_link == rss[0].links[-1].href:
            return None

    if filter_last:
        rss = _filter_last_anime(rss, last_title_link)

    parsed_data = list()

    for entry in rss:
        entry.title = entry.title.split('/')  # Разделение строки на Ру-название, серии и ориг. название
        parsed_data.append({
            "name": entry.title[0],
            "original_name": entry.title[-1],
            "description": entry.summary,
            "episode_count": entry.categoy[entry.categoy.find("(") + 1:entry.categoy.find("эп")].replace(" ", ""),
            "current_episode": _find_current_episode(entry.title[1]),
            "darklibria_link": entry.link,
            "download_link": {
                "type": entry.title[1][entry.title[1].find("[")+1:entry.title[1].find("]")],
                "link": entry.links[-1].href,
                "date_added": entry.published
            }
        })
    return parsed_data
