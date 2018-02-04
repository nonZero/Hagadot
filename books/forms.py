from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from . import models


class RowsRangeForm(forms.Form):
    start = forms.IntegerField(min_value=1)
    end = forms.IntegerField(min_value=1)

    def clean(self):
        data = super().clean()
        if 'start' in data and 'end' in data:
            if not data['start'] <= data['end']:
                raise ValidationError(_("Invalid range"))
        return data


class AnnotationCreateForm(forms.ModelForm):
    class Meta:
        model = models.Annotation
        fields = (
            'x',
            'y',
            'content',
        )
        widgets = {
            'x': forms.HiddenInput(),
            'y': forms.HiddenInput(),
        }


class BookImportForm(forms.Form):
    doc_id = forms.CharField(
        max_length=100, validators=[
            RegexValidator(r'^[-\w]+$')
        ],
        help_text=_("For example: PNX_MANUSCRIPTS000041667-2")
    )
