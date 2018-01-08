from django.contrib import admin

from . import models


class PageInline(admin.TabularInline):
    model = models.Page


class BookAdmin(admin.ModelAdmin):
    inlines = (
        # PageInline,
    )
    readonly_fields = (
        'doc_id',
        'num_pages',
    )


admin.site.register(models.Book, BookAdmin)
