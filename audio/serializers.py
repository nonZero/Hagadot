from django.utils.html import linebreaks
from rest_framework import serializers

from . import models


class TrackSerializer(serializers.ModelSerializer):
    bookmarks = serializers.SlugRelatedField('ordinal', many=True,
                                             read_only=True)
    summary = serializers.SerializerMethodField()

    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'audio_url',
            'length',
            'summary',
            'bookmarks',
        )

    def get_summary(self, obj):
        return linebreaks(obj.summary)
