"""Forms(limits) for models in quotesapp

The Meta class provides information on which model the form is associated with,
which fields are included or excluded, and any widgets used to customize field
appearance.
"""
from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    """A form for creating or updating tags.

    This form allows users to create or modify tags used to categorize quotes.
    Each tag must have a unique name.

    Attributes:
        name (CharField): The name of the tag. Must be between 3 and 25
            characters long and is required.

    Meta:
        model (Tag): The model associated with this form.
        fields (list): Specifies which fields to include in the form.
            In this case, only the 'name' field.
    """
    name = CharField(
        min_length=3,
        max_length=25,
        required=True,
        widget=TextInput()
    )

    class Meta:
        """meta"""
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    """A form for creating or updating authors.

    This form allows users to create or modify authors who have written or
    said quotes. Each author must have a unique name.

    Attributes:
        name (CharField): The name of the author. Must be between 3 and 120
            characters long and is required.

    Meta:
        model (Author): The model associated with this form.
        fields (list): Specifies which fields to include in the form. In this
            case, only the 'name' field.
    """
    name = CharField(
        min_length=3,
        max_length=120,
        required=True,
        widget=TextInput()
    )

    class Meta:
        """meta"""
        model = Author
        fields = ['name']


class QuoteForm(ModelForm):
    """A form for creating or updating quotes.

    This form allows users to create or modify quotes attributed to authors.
    Each quote must have associated author information and text.

    Attributes:
        author (CharField): The name of the author of the quote. This field is
            a free text input and should be an existing author. (Note: This
            may need to be adjusted for use in practice.)
        text (CharField): The text of the quote. Must be between 10 and 250
            characters long and is required.

    Meta:
        model (Quote): The model associated with this form.
        fields (list): Specifies which fields to include in the form.
            In this case, only the 'text' field.
        exclude (list): Specifies which fields to exclude from the form.
            In this case, 'tags' and 'author' fields are excluded as they are
            handled separately.
        widgets (dict): Customizes the appearance of form fields. Here,
            the 'text' field is rendered as a textarea with specified rows
            and columns.
    """
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
        """meta"""
        model = Quote
        fields = ['text']
        exclude = ['tags', 'author']
        widgets = {
            'text': Textarea(attrs={'rows': 4, 'cols': 40}),
        }
