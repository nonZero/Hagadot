from django.views.generic import ListView, DetailView

from hagadot.base_views import SimpleJsonView
from . import models


class BookmarkListView(ListView):
    model = models.Bookmark


class BookmarkDetailView(DetailView):
    model = models.Bookmark


class RowListView(ListView):
    model = models.Row


class BookmarksAPIView(SimpleJsonView):
    def get_data(self):
        roots = models.Bookmark.objects.root_nodes()
        rows = [(r.ordinal, r.content) for r in models.Row.objects.all()]

        return {
            'bookmarks': list(roots[0].walk()),
            'rows': rows,
        }
