from django.db import models
from django.urls import reverse
from mptt.fields import TreeManyToManyField

from bookmarks.models import Bookmark
from books.nli_api import get_img_url, get_thumb_url


class Book(models.Model):
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=100, unique=True)
    doc_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:detail', args=[str(self.id)])


class Page(models.Model):
    THUMB_HEIGHT = 100

    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='pages')
    ordinal = models.PositiveIntegerField()
    img_id = models.CharField(max_length=100, unique=True)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()

    bookmarks = TreeManyToManyField(Bookmark, blank=True, related_name='pages')

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

    def get_absolute_url(self):
        return reverse('books:page', args=(self.book_id, self.ordinal))

    def preview_url(self):
        return get_img_url(self.img_id)

    def thumb_url(self):
        return get_thumb_url(self.img_id, self.THUMB_HEIGHT)

    def thumb_width(self):
        return int(self.THUMB_HEIGHT / self.height * self.width)
