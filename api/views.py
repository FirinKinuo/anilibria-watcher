from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializer import *
from watcher import models


class AllAnimeView(ListAPIView):
    queryset = models.AnimeDownloadLink.objects
    serializer_class = AnimeDownloadLinkSerializer


class AnimeView(RetrieveAPIView):
    queryset = models.AnimeDownloadLink.objects
    serializer_class = AnimeDownloadLinkSerializer


