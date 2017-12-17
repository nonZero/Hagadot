import logging

from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction

from books import nli_api
from books.models import Book
from books.nli_api import fix_pages


class Command(BaseCommand):
    help = "Import a book from NLI API"

    def add_arguments(self, parser):
        parser.add_argument('doc_id')

    def handle(self, doc_id, **options):
        if options['verbosity'] >= 2:
            logging.basicConfig(level=logging.DEBUG)
        doc = nli_api.get_manifest(doc_id)
        pages = nli_api.get_pages_from_manifest(doc)
        pages = list(fix_pages(pages))
        if len(pages) == 0:
            raise CommandError("No pages found for doc.")

        title = doc['label']
        with transaction.atomic():
            b = Book.objects.create(
                title=title,
                slug=doc_id,
                doc_id=doc_id,
                num_pages=len(pages),
            )
            for p in pages:
                b.pages.create(
                    ordinal=p['ordinal'],
                    img_id=p['id'],
                    height=p['height'],
                    width=p['width'],
                )
