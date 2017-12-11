from django.views.generic import ListView, DetailView, TemplateView

from . import models


class HomeView(TemplateView):
    template_name = "home.html"

class BookListView(ListView):
    model = models.Book


class BookDetailView(DetailView):
    model = models.Book
