from anilibria_watcher.celery import celery_app
from .logic import update_anime_data


@celery_app.task
def background_update_anime() -> None:
    """
    Celery задача, вызывает функцию по обновлению БД
    :return: None
    """

    update_anime_data()
