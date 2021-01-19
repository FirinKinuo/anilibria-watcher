from django.contrib import admin

from .models import *

admin.site.register(Anime)
admin.site.register(AnimeDownloadLink)
admin.site.register(UserFavorite)