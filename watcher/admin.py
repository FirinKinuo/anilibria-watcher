from django.contrib import admin

from .models import *

admin.site.register(Anime)
admin.site.register(User)
admin.site.register(UserFavorite)
