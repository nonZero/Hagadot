import json

from django.core.management.base import BaseCommand
from django.utils.html import linebreaks

from bookmarks.models import Bookmark
from books.models import Book, Page, Annotation


def get_ann(a: Annotation):
    return {
        'id': a.id,
        'x': float(a.x),
        'y': float(a.y),
        'content': linebreaks(a.content),
    }


def get_page(p: Page):
    return {
        'ordinal': p.ordinal,
        'rows': [r.ordinal for r in p.rows.all()],
        'annotations': [get_ann(a) for a in p.annotations.all()],
    }


def get_books_with_rows():
    for b in Book.objects.all():
        yield {
            'id': b.id,
            'doc_id': b.doc_id,
            'summary': b.summary,
            'num_pages': b.num_pages,
            'start_page': 3,
            'end_page': b.num_pages,
            'pages': [
                get_page(p) for p in
                b.pages.order_by('ordinal')]
        }


class Command(BaseCommand):
    help = "Export books"

    def handle(self, *args, **options):
        data = list(get_books_with_rows())
        print(json.dumps(data, indent=2))
