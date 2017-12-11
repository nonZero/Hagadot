import json
from django.db import models
from django.urls import reverse
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Bookmark(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True,
                            on_delete=models.CASCADE)

    ordinal = models.IntegerField()
    title = models.CharField(max_length=300)
    content_json = models.TextField(null=True)

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

    def content_text(self):
        if not self.content_json:
            return ""
        return "\n".join(json.loads(self.content_json))

    def content_html(self):
        return mark_safe(linebreaks(self.content_text()))


