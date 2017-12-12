from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView

from books import forms
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

    def form(self):
        return forms.AddBookmarkForm()

    def post(self, request, **kwargs):
        o = self.get_object()
        form = forms.AddBookmarkForm(request.POST)
        if not form.is_valid():
            return self.get(request, **kwargs)
        o.bookmarks.add(form.cleaned_data['bookmark'])
        return redirect(o)
