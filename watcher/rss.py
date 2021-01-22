import feedparser
import datetime


def _find_current_episode(dirty_str: str) -> int:
    """
    Поиск текущего эпизода
    :param dirty_str: Грязная строка с лишними данными, из которой надо вытянуть число
    :return: Возвращает int с текущей серией
    """

    try:
        return int(dirty_str.split('-')[1][0])
    except IndexError:
        # Если в тайтле вышла первая серия, то поиск разделением не получится
        return int(dirty_str[dirty_str.find(":")+1:dirty_str.find("[")].replace(" ", ""))


def _filter_last_anime(rss: list, last_title_date: str) -> list:
    """
    Возращает отфильтрованный до последнего тайтла в записи список аниме
    :param rss: Список RSS для фильтрации
    :param last_title_date: Дата последнего тайтла
    :return: Отфильтрованный список RSS
    """

    """
    Немного пояснения за следующий костыль:
    Каким то магическим образом, строка из RSS
    Не является идентичной такой же строке из БД, поэтому последующий код не имел смысла и он тупо
    Отправлял все, что было в RSS, от отделяя новое от старого, приведение к типу datetime
    Позволило божественному Python понять, что даты то одинаковые, че дальше шакалиться
    """

    date_in_db = datetime.datetime.strptime(last_title_date, '%Y-%m-%d %H:%M:%S')

    for i, el in enumerate(rss):
        date_in_rss = datetime.datetime.strptime(el.published, '%Y-%m-%d %H:%M:%S')
        if date_in_rss == date_in_db:
            return rss[:i]
        return rss


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
