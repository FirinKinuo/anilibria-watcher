from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    webhooks_urls = models.JSONField(null=True, verbose_name="Ссылки на webhooks")


class Anime(models.Model):
    """Таблица с аниме"""
    anilibria_id = models.IntegerField(verbose_name="ID Anilibria")
    original_name = models.TextField(verbose_name="Оригинальное название")
    updated_at = models.BigIntegerField(verbose_name="Дата последнего обновления")

    def __str__(self):
        return f"{self.anilibria_id} -> {self.original_name}"

    class Meta:
        verbose_name = "Тайтл"
        verbose_name_plural = "Аниме"
        ordering = ["anilibria_id"]


class UserFavorite(models.Model):
    """
    Таблица с избранным пользователя
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name="Аниме")

    def __str__(self):
        return f"{self.user} >> {self.anime}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
