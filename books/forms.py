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
            'track',
            'content',
        )
        widgets = {
            'x': forms.HiddenInput(),
            'y': forms.HiddenInput(),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = (
            'title',
            'summary',
            'short_summary',
            'start_page',
            'end_page',
            'cover_image',
        )

    def clean_start_page(self):
        v = self.cleaned_data['start_page']
        if v > self.instance.num_pages:
            raise ValidationError(
                _("Start page must be smaller than total pages."))
        return v

    def clean_end_page(self):
        v = self.cleaned_data['end_page']
        if v > self.instance.num_pages:
            raise ValidationError(
                _("End page must be smaller than total pages."))
        return v

    def clean(self):
        data = super().clean()
        if 'start_page' in data and 'end_page' in data and data['start_page'] > \
                data['end_page']:
            raise ValidationError(_("Start page must be smaller than end page."))

        return data


class BookImportForm(forms.Form):
    doc_id = forms.CharField(
        max_length=100, validators=[
            RegexValidator(r'^[-\w]+$')
        ],
        help_text=_("For example: PNX_MANUSCRIPTS000041667-2")
    )
