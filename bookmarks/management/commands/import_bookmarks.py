import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from bookmarks.models import Bookmark


def walk(texts, node, i=0, parent=None, path=None):
    if path is None:
        path = path or []
    indent = len(path)
    print('-', indent * "  ", node['enTitle'])
    text = None
    if 'nodes' not in node:
        d = texts
        for k in path:
            d = d[k]
        text = json.dumps(d)

    parent = Bookmark.objects.create(
        parent=parent,
        ordinal=i,
        title=node['heTitle'],
        content_json=text,
    )
    if 'nodes' in node:
        for i, n in enumerate(node['nodes']):
            walk(texts, n, i, parent, path + [n['enTitle']])


class Command(BaseCommand):
    help = "Load haggadah bookmarks and text."

    def handle(self, *args, **options):
        with (Path(settings.BASE_DIR) / "data/haggadah.json").open() as f:
            data = json.load(f)
        with transaction.atomic():
            walk(data['text'], data['schema'])
