from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from . import models

RE_DETAILS_URL = r"^https://archive.org/details/[-\w]+"


class TrackImportForm(forms.Form):
    details_url = forms.URLField(
        label=_(
            "archive.org item details url ( https://archive.org/details/... )"),
        validators=[RegexValidator(RE_DETAILS_URL,
                                   message="Please use https://archive.org/details/....")],

    )


class TrackBookmarksForm(forms.ModelForm):
    class Meta:
        model = models.Track
        fields = (
            'bookmarks',
        )
        widgets = {
            'bookmarks': forms.CheckboxSelectMultiple,
        }
