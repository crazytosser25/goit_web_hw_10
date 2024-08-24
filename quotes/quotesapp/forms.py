from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(
        min_length=3,
        max_length=25,
        required=True,
        widget=TextInput()
    )

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    name = CharField(
        min_length=3,
        max_length=120,
        required=True,
        widget=TextInput()
    )

    class Meta:
        model = Author
        fields = ['name']


class QuoteForm(ModelForm):

    author = CharField(
        max_length=120,
        required=True,
        widget=TextInput()
    )
    text = CharField(
        min_length=10,
        max_length=250,
        required=True,
        widget=Textarea()
    )

    class Meta:
        model = Quote
        fields = ['text']
        exclude = ['tags', 'author']
        widgets = {
            'text': Textarea(attrs={'rows': 4, 'cols': 40}),
        }
