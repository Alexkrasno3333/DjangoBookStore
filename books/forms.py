from django import forms
from django.forms import ModelForm

from books.models import BookSuggestion

from .models import Book

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        label="Search"
    )


class BookSuggestionForm(ModelForm):
   class Meta:
        model = BookSuggestion
        fields = ["name", "email", "book_title", "author", "message"]


class BookFormDet(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "price", "stock", "description"]
    