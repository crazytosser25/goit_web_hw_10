"""Models for quotesapp"""
from django.db import models


class Tag(models.Model):
    """Represents a tag that can be associated with quotes.

    This model defines tags that can be used to categorize or label quotes.
    Each tag has a unique name.

    Attributes:
        name (CharField): The name of the tag, which must be unique and can be
        up to 60 characters long.

    Methods:
        __str__: Returns a string representation of the tag, which is its name.
    """
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    """Represents an author of quotes.

    This model defines authors who have written or said quotes. Each author
    has a unique name.

    Attributes:
        name (CharField): The name of the author, which must be unique and
        can be up to 120 characters long.

    Methods:
        __str__: Returns a string representation of the author, which is their
            name.
    """
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    """Represents a quote attributed to an author.

    This model defines quotes along with the associated author and tags.
    Each quote contains the text of the quote, a reference to the author,
    and a list of tags.

    Attributes:
        author (ForeignKey): A reference to the Author model indicating
            who said or wrote the quote. This field is required and uses
            a default value of the author with ID 1.
        text (CharField): The text of the quote, which must be provided and
            can be up to 3000 characters long.
        tags (ManyToManyField): A list of tags associated with the quote,
            allowing multiple tags to be linked.

    Methods:
        __str__: Returns a string representation of the quote, which includes
            the quote text and the name of the author.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=3000, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.text}\nBy {self.author.name}"
