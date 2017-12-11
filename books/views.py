from django.views.generic import ListView, DetailView

from . import models


class BookListView(ListView):
    model = models.Book


class BookDetailView(DetailView):
    model = models.Book
