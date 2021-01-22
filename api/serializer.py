from rest_framework import serializers

from watcher import models


class AnimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Anime
        fields = "__all__"


class AnimeDownloadLinkSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer(many=False, read_only=True)

    class Meta:
        model = models.AnimeDownloadLink
        fields = "__all__"


class UserFavorite(serializers.ModelSerializer):
    class Meta:
        model = models.UserFavorite
        fields = "__all__"

