import logging

from django.core.management.base import BaseCommand, CommandError

from books.importer import import_book


class Command(BaseCommand):
    help = "Import a book from NLI API"

    def add_arguments(self, parser):
        parser.add_argument('doc_id')

    def handle(self, doc_id, **options):
        if options['verbosity'] >= 2:
            logging.basicConfig(level=logging.DEBUG)
        try:
            import_book(doc_id)
        except ValueError as e:
            raise CommandError(*e.args) from e
