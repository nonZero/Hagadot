from django.contrib import admin

from . import models


class PageInline(admin.TabularInline):
    model = models.Page


class BookAdmin(admin.ModelAdmin):
    inlines = (
        PageInline,
    )


admin.site.register(models.Book, BookAdmin)
