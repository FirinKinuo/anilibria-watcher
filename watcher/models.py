from django.db import models
from django.contrib.auth.models import User


class Anime(models.Model):
    """Таблица с аниме"""
    name = models.TextField(verbose_name="Название")
    original_name = models.TextField(verbose_name="Оригинальное название")
    description = models.TextField(null=True, verbose_name="Описание")
    episode_count = models.CharField(max_length=9, null=True, verbose_name="Количество эпизодов")
    current_episode = models.IntegerField(default=0, verbose_name="Текущий эпизод")
    darklibria_link = models.URLField(verbose_name="Ссылка на страницу Dark-Libria.it")

    def __str__(self):
        return f"{self.name} / {self.original_name}"

    class Meta:
        verbose_name = "Тайтл"
        verbose_name_plural = "Аниме"
        ordering = ["name"]


class AnimeDownloadLink(models.Model):
    """
    Ссылки для скачивания серий по торренту
    Так как обычно файлов торрента несколько, в зависимости от качества, кодировки, серий и прочего,
    то необходимо предоставлять несколько ссылок
    """

    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="ID аниме")
    type = models.TextField(verbose_name="Тип торрента")
    link = models.URLField(verbose_name="Ссылка")
    date_added = models.DateTimeField(verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.anime} -- {self.type}"

    class Meta:
        verbose_name = "Ссылка на скачивание"
        verbose_name_plural = "Ссылки на скачивание"
        ordering = ['anime']


class UserFavorite(models.Model):
    """
    Таблица с избранным пользователя
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")

    def __str__(self):
        return f"{self.user_id} >> {self.anime_id}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
