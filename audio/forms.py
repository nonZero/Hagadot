from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

RE_DETAILS_URL = r"^https://archive.org/details/[-\w]+"


class TrackImportForm(forms.Form):
    details_url = forms.URLField(
        label=_(
            "archive.org item details url ( https://archive.org/details/... )"),
        validators=[RegexValidator(RE_DETAILS_URL,
                                   message="Please use https://archive.org/details/....")],

    )
