"""_summary_

Returns:
    _type_: _description_
"""
from django.db import models


class Tag(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=3000, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.text}\nBy {self.author.name}"
