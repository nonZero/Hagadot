from django import forms
from mptt.forms import TreeNodeChoiceField

from bookmarks.models import Bookmark


class AddBookmarkForm(forms.Form):
    bookmark = TreeNodeChoiceField(Bookmark.objects.all())
