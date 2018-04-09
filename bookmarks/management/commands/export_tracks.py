import json

from django.core.management.base import BaseCommand

from audio.models import Track


def get_tracks():
    for t in Track.objects.all():
        yield {
            'id': t.id,
            'title': t.title,
            'audio_url': t.audio_url,
            'length': float(t.length),
            'summary': t.summary,
            'bookmarks': [bm.ordinal for bm in t.bookmarks.all()]
        }


class Command(BaseCommand):
    help = "Export tracks"

    def handle(self, *args, **options):
        data = list(get_tracks())
        print(json.dumps(data, indent=2))
