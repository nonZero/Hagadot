from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeManyToManyField

from bookmarks.models import Bookmark


class Track(models.Model):
    title = models.CharField(_("title"), max_length=300)
    audio_url = models.URLField(_("audio url"), unique=True, max_length=600)
    length = models.DecimalField(_("length"), max_digits=10, decimal_places=2,
                                 help_text=_("in seconds"))
    summary = models.TextField(_("summary"), null=True, blank=True)
    doc_id = models.CharField(_("NLI document ID"), max_length=100,
                              unique=True, null=True,
                              blank=True)

    bookmarks = TreeManyToManyField(Bookmark, related_name='tracks',
                                    blank=True)

    class Meta:
        verbose_name = _("track")
        verbose_name_plural = _("tracks")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('audio:detail', args=[str(self.id)])

    def length_str(self):
        return "{:01.0f}:{:02.0f}".format(*divmod(self.length, 60))
