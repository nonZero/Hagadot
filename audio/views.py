from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import SUCCESS, WARNING
from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, UpdateView, FormView

from audio.archive_org_api import get_audio_info
from audio.models import Track
from . import forms
from . import models


class TrackListView(ListView):
    model = models.Track


class TrackDetailView(DetailView):
    model = models.Track


class TrackImportView(PermissionRequiredMixin, FormView):
    permission_required = "audio.add_track"
    form_class = forms.TrackImportForm
    template_name = "audio/track_import.html"

    def form_valid(self, form):
        info = get_audio_info(form.cleaned_data['details_url'])
        if not info:
            form.add_error('details_url', _("can't download info"))
            return self.form_invalid(form)
        t, created = Track.objects.get_or_create(
            audio_url=info['url'], defaults=dict(
                title=info['title'][:300],
                length=info['length'],
                summary=strip_tags(info['description']),
            )
        )
        msg = _("Track imported successfully") if created else _(
            "Track already exists")
        level = SUCCESS if created else WARNING
        messages.add_message(self.request, level, msg)
        return redirect(t)


# class TrackCreateView(PermissionRequiredMixin, CreateView):
#     permission_required = "audio.add_track"
#     model = models.Track
#     fields = (
#         'title',
#         'audio_url',
#         'length',
#         'summary',
#         'doc_id',
#     )
#

class TrackUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "audio.change_track"
    model = models.Track
    fields = (
        'title',
        'audio_url',
        'summary',
        'doc_id',
        'length',
    )

class TrackUpdateBookmarksView(PermissionRequiredMixin, UpdateView):
    permission_required = "audio.change_track"
    model = models.Track
    form_class = forms.TrackBookmarksForm

