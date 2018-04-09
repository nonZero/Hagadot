from django.utils.html import linebreaks
from rest_framework import serializers

from audio.serializers import TrackSerializer
from . import models


class AnnotationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    track = TrackSerializer()

    class Meta:
        model = models.Annotation
        fields = (
            'type',
            'id',
            'x',
            'y',
            'content',
            'track',
        )

    def get_type(self, obj):
        return 'audio' if obj.track_id else 'text'

    def get_content(self, obj):
        return linebreaks(obj.content)


class PageSerializer(serializers.ModelSerializer):
    rows = serializers.SlugRelatedField('ordinal', many=True, read_only=True)
    annotations = AnnotationSerializer(many=True)

    class Meta:
        model = models.Page
        fields = (
            'ordinal',
            'rows',
            'annotations',
        )


class BookSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True)

    class Meta:
        model = models.Book
        fields = (
            'id',
            'doc_id',
            'summary',
            'short_summary',
            'num_pages',
            'start_page',
            'end_page',
            'pages',
        )
