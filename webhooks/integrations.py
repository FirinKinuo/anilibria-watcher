from dhooks import Embed, Webhook


def _discord_integration(url: str, content: dict) -> None:
    """
    Интеграция с вебхуками discord, отправляет информацию по новому тайтлу
    по ссылке на вебхук
    :param url: Ссылка на вебхук
    :param content Информация по тайтлу:
    :return: None
    """

    # TODO: Избавиться от dhooks, когда не будет лень
    hook = Webhook(url=url)

    embed = Embed(color=0x11f275)
    embed.add_field(name=f"{content['name']}",
                    value=f"{content['original_name']}\n"
                          f"Текущая: **{content['current_episode']}**\n"
                          f"Всего: **{content['episode_count']}**",
                    inline=False)
    embed.add_field(name="Страница",
                    value=content['darklibria_link'],
                    inline=False)
    embed.add_field(name="Скачать",
                    value=f"[{content['download_link']['type']}] {content['download_link']['link']}",
                    inline=False)

    hook.send(embed=embed)


def find_integrations_and_send(url: str, content: dict) -> bool:
    """
    Ищет возможные интеграции с сервисами и отправляет удобный им вариант webhook
    :param url: Ссылка на вебхук
    :param content: Словарь с данными
    :return: None
    """
    # TODO: Переделать интеграции под новую структуру БД
    # Заглушка пока я не переделаю под новую структуру
    return False

    if url.find("https://discord.com/api/webhooks/") != -1:
        _discord_integration(url, content)
        return True
    else:
        return False
