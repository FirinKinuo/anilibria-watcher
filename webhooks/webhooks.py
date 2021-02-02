import requests
from .integrations import find_integrations_and_send


def _send(link: str, content: (dict, list)) -> None:
    """
    Служебная функция для отправки вебхуков
    :param link: Ссылка на вебхук
    :param content: Словарь или список словарей с контентом для отправки вебхуков
    :return: None
    """
    if isinstance(content, dict):  # Если content - словарь, то отправляем прям так
        if not find_integrations_and_send(link, content):
            requests.post(link, data={'content': f'{content}'})
    elif isinstance(content, list):  # Иначе, если  content - список, то отправляем его каждый элемент
        for data in content:
            if not find_integrations_and_send(link, data):
                requests.post(link, data={'content': f'{data}'})


def send_webhook(webhook_url: (str, dict), content: (dict, list)) -> None:
    """
    Отправляет вебхук по указанной ссылке
    :param webhook_url: Ссылка на Webhook пользователя или список ссылок
    :param content: Список словарей или словарь с данными для отправки через webhook
    :return: None
    """

    if isinstance(webhook_url, str):
        _send(webhook_url, content)
    elif isinstance(webhook_url, dict):
        for link in webhook_url['links']:
            _send(link, content)
