from rest_framework import serializers

from watcher import models


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Anime
        fields = ('anilibria_id',)


class UserFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserFavorite
        fields = "__all__"
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'username',
            'webhooks_urls'
        )

