from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from . import models


class HomeView(TemplateView):
    template_name = "home.html"


class BookListView(ListView):
    model = models.Book


class BookDetailView(DetailView):
    model = models.Book


class PageDetailView(DetailView):
    model = models.Page

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, book_id=self.kwargs['pk'],
                                 ordinal=self.kwargs['ordinal'])
