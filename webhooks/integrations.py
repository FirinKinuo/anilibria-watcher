from dhooks import Webhook, Embed


def _discord_integration(url: str, content: dict):
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


def find_integrations_and_send(url: str, content=dict) -> bool:
    """

    :param str url:
    :param dict content :
    :return:
    """
    if url.find("https://discord.com/api/webhooks/") != -1:
        _discord_integration(url, content)
        return True
    else:
        return False
