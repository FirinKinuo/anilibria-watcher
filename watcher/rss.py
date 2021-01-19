import feedparser
import datetime


def _replace_symbols_episode(episode_string: str) -> int:
    """
    Заменяет специальные символы в строке с количеством эпизодов на соотвествующее значение int
    :param episode_string: Строка с количеством эпизодов
    :return: Возвращает количество эпизодов в тайтле
    """
    try:
        if episode_string.find("∞") != -1:
            return -1
        elif episode_string.find("?") != -1:
            return 0
        else:
            return int(episode_string)
    except ValueError as err:
        with open("log.log", 'a') as file:
            file.write(f"replace err -> {err}")


def _filter_last_anime(rss: list, last_title_date: str) -> list:
    """
    Возращает отфильтрованный до последнего тайтла в записи список аниме
    :param rss: Список RSS для фильтрации
    :param last_title_date: Дата последнего тайтла
    :return: Отфильтрованный список RSS
    """
    for i, el in enumerate(rss):
        if el.published == last_title_date:
            return rss[:i]


def parse_anilibria_rss(last_title_date=None, filter_last=False) -> (list, bool):
    """
    Получить готовый список с данными по последним 30 тайтлам в списке

    :param last_title_date: Дата добавления последнего тайтла для проверки на обновление списка
    :param filter_last: Проводить ли фильтрацию до последнего записанного тайтла, необходим last_title_date
    :return: Возвращает список последних в RSS тайтлов, либо False, если нет новых тайтлов
    """
    rss = feedparser.parse("https://dark-libria.it/rss.xml").entries

    if last_title_date is not None:
        last_title_date = datetime.datetime.strftime(last_title_date, '%Y-%m-%d %H:%M:%S')

        if last_title_date == rss[0].published:
            return False

    if filter_last:
        rss = _filter_last_anime(rss, last_title_date)

    parsed_data = list()

    for entry in rss:
        entry.title = entry.title.split('/')  # Разделение строки на Ру-название, серии и ориг. название
        parsed_data.append({
            "name": entry.title[0],
            "original_name": entry.title[-1],
            "description": entry.summary,
            "episode_count": _replace_symbols_episode(
                entry.categoy[entry.categoy.find("(") + 1:entry.categoy.find("эп")]),
            "current_episode": int(entry.title[1].split('-')[1][0]),
            "darklibria_link": entry.link,
            "download_link": {
                "type": entry.title[1][entry.title[1].find("[")+1:entry.title[1].find("]")],
                "link": entry.links[-1].href,
                "date_added": entry.published
            }
        })
    return parsed_data
