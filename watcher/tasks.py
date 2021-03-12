from anilibria_watcher.celery import celery_app

import watcher.logic as logic


@celery_app.task
def background_rss_anilibria() -> None:
    """
    Celery задача, вызывает функцию по обновлению БД
    :return: None
    """
    anime_data = logic.get_anime_data_from_api()
    if anime_data:
        logic.add_anime_data(anime_data)
        logic.send_webhooks_to_users(anime_data)
