import requests


def send_webhook(webhook_url: (str, list), content: dict) -> None:
    """
    Отправляет вебхук по указанной ссылке
    :param webhook_url: Ссылка на Webhook пользователя или список ссылок
    :param content: dict с данными для отправки через webhook
    :return: None
    """
    if isinstance(webhook_url, str):
        requests.post(webhook_url, data={'content': f'{content}'})
    elif isinstance(webhook_url, list):
        for link in webhook_url:
            requests.post(link, data={'content': f'{content}'})
