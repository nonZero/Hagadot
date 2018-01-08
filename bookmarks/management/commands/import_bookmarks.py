import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from bookmarks.models import Bookmark, Row


def walk(texts, node, i=0, parent=None, path=None):
    if path is None:
        path = path or []
    indent = len(path)
    print('-', indent * "  ", node['enTitle'])
    parent = Bookmark.objects.create(
        parent=parent,
        ordinal=i,
        title=node['heTitle'],
    )
    i += 1
    if 'nodes' in node:
        for n in node['nodes']:
            i = walk(texts, n, i, parent, path + [n['enTitle']])
    else:
        d = texts
        for k in path:
            d = d[k]
        for row in d:
            Row.objects.create(
                bookmark=parent,
                ordinal=i,
                content=row,
            )
            i += 1
    return i


class Command(BaseCommand):
    help = "Load haggadah bookmarks and text."

    def handle(self, *args, **options):
        with (Path(settings.BASE_DIR) / "data/haggadah.json").open() as f:
            data = json.load(f)
        with transaction.atomic():
            walk(data['text'], data['schema'])
