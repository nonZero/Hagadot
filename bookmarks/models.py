from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Bookmark(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True,
                            on_delete=models.CASCADE)

    ordinal = models.IntegerField()
    title = models.CharField(max_length=300)

    class Meta:
        unique_together = (
            ('parent', 'ordinal'),
        )

    class MPTTMeta:
        order_insertion_by = ['ordinal']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookmarks:detail', args=[str(self.id)])

    def walk(self):
        for c in self.get_children():
            d = {
                'title': c.title,
                'ordinal': c.title,
            }
            l = list(c.walk())
            if l:
                d['children'] = l
            l = list(c.rows.values_list('ordinal', flat=True))
            if l:
                d['rows'] = l
            yield d


class Row(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE,
                                 related_name='rows')
    ordinal = models.IntegerField(unique=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.ordinal} {self.bookmark}"

    # def get_absolute_url(self):
    #     return reverse('bookmarks:detail', args=[str(self.id)])

    class Meta:
        ordering = (
            "ordinal",
        )
