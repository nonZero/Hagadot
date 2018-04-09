from django.db import transaction

from books import nli_api
from books.models import Book
from books.nli_api import fix_pages


def import_book(doc_id):
    doc = nli_api.get_manifest(doc_id)
    pages = nli_api.get_pages_from_manifest(doc)
    pages = list(fix_pages(pages))
    if len(pages) == 0:
        raise ValueError("No pages found for doc.")
    title = doc['label']
    with transaction.atomic():
        b = Book.objects.create(
            title=title,
            slug=doc_id,
            doc_id=doc_id,
            num_pages=len(pages),
            start_page=1,
            end_page=len(pages),
        )
        for p in pages:
            b.pages.create(
                ordinal=p['ordinal'],
                img_id=p['id'],
                height=p['height'],
                width=p['width'],
            )
    return b
