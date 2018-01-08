from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView

from bookmarks.models import Row
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

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            start_row = self.object.rows.first()
            end_row = self.object.rows.last()
            prev_pagerow = models.Page.rows.through.objects.order_by(
                'row__ordinal').filter(
                page__book=self.object.book,
                page__ordinal__lt=self.object.ordinal).last()
            if prev_pagerow:
                rows = Row.objects.filter(
                    ordinal__gte=prev_pagerow.row.ordinal)
            else:
                rows = Row.objects.all()
            d.update({
                'start_row': start_row,
                'end_row': end_row,
                'rows': rows[:60],
            })
        return d

    def post(self, request, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        o = self.get_object()
        form = forms.RowsRangeForm(request.POST)
        if not form.is_valid():
            self.errors = form.errors
            return self.get(request, **kwargs)
        rows = Row.objects.filter(
            ordinal__gte=form.cleaned_data['start'],
            ordinal__lte=form.cleaned_data['end'],
        )
        o.rows.set(rows)
        if request.POST.get('continue') == 'next':
            o = o.next_page_url()
            if not o:
                o = self.get_object()
        return redirect(o)
