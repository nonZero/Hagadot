from django.views.generic import ListView, DetailView

from . import models


class BookmarkListView(ListView):
    model = models.Bookmark


class BookmarkDetailView(DetailView):
    model = models.Bookmark


class RowListView(ListView):
    model = models.Row