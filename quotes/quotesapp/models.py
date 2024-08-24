from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=250, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.text}\nBy {self.author.name}"
