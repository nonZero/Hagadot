from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from audio.models import Track
from bookmarks.models import Bookmark, Row
from books.nli_api import get_img_url, get_thumb_url


class Book(models.Model):
    title = models.CharField(_("title"), max_length=300)
    slug = models.CharField(max_length=100, unique=True)
    doc_id = models.CharField(max_length=100, unique=True)
    summary = models.TextField(_("summary"), null=True, blank=True)
    short_summary = models.CharField(_("short summary"), max_length=400,
                                     null=True, blank=True)

    num_pages = models.PositiveIntegerField(null=True)

    start_page = models.PositiveIntegerField(_("start page"), null=True)
    end_page = models.PositiveIntegerField(_("end page"), null=True)

    cover_image = models.ImageField(_("cover image"), null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:detail', args=[str(self.id)])

    def annotations(self):
        return Annotation.objects.filter(page__book=self)


class Page(models.Model):
    THUMB_HEIGHT = 100

    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='pages')
    ordinal = models.PositiveIntegerField()
    img_id = models.CharField(max_length=100, unique=True)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()

    rows = models.ManyToManyField(Row, blank=True, related_name='pages')

    class Meta:
        unique_together = (
            ('book', 'ordinal'),
        )
        ordering = (
            'book',
            'ordinal',
        )

    def __str__(self):
        return f"{self.book} [#{self.ordinal}]"

    def get_absolute_url(self, d=0):
        return reverse('books:page', args=(self.book_id, self.ordinal + d))

    def preview_url(self):
        return get_img_url(self.img_id)

    def thumb_url(self):
        return get_thumb_url(self.img_id, self.THUMB_HEIGHT)

    def thumb_width(self):
        return int(self.THUMB_HEIGHT / self.height * self.width)

    def is_first(self):
        return self.ordinal == 1

    def is_last(self):
        return self.ordinal == self.book.num_pages

    def prev_page_url(self):
        return self.get_absolute_url(-1)

    def next_page_url(self):
        return self.get_absolute_url(1)

    def get_bookmarks(self):
        return Bookmark.objects.filter(rows__in=self.rows.all())

    def get_tracks(self):
        return Track.objects.filter(bookmarks__in=self.get_bookmarks())


class Annotation(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='annotations')
    x = models.DecimalField(max_digits=5, decimal_places=1)
    y = models.DecimalField(max_digits=5, decimal_places=1)
    track = models.ForeignKey(Track, null=True, blank=True,
                              on_delete=models.CASCADE,
                              related_name="annotations")
    content = models.TextField(_("content"))

    def __str__(self):
        return f"#{self.page.book.id}:{self.page.id}:{self.id} [{self.x}%:{self.y}%]"
