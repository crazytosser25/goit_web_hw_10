from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    name = models.CharField(max_length=120, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ManyToManyField(Author)
    text = models.CharField(max_length=250, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.text}\nBy {self.author}"
