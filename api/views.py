from django.shortcuts import render
from watcher.logic import update_anime_data


def fill(request):
    update_anime_data()
