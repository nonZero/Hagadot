from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


class BookmarkAdmin(MPTTModelAdmin):
    fields = (
        'parent',
        'ordinal',
        'title',
    )
    readonly_fields = (
        'parent',
        'ordinal',
        'title',
    )


admin.site.register(models.Bookmark, BookmarkAdmin)
