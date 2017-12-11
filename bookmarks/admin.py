from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


class BookmarkAdmin(MPTTModelAdmin):
    fields = (
        'parent',
        'ordinal',
        'title',
        'content_html',
    )
    readonly_fields = (
        'content_html',
    )


admin.site.register(models.Bookmark, BookmarkAdmin)
