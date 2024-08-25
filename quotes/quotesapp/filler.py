"""Script to save quotes from MongoDB to Postgres.
"""
import os
from mongoengine import connect, Document
from mongoengine.fields import ReferenceField, ListField, StringField
from dotenv import load_dotenv
from django.db import transaction
from .models import Tag, Author, Quote
# pylint: disable=no-member


load_dotenv('../.env')
mongo_user = os.getenv('MONGO_USER')
mongodb_pass = os.getenv('MONGO_PASSWORD')
db_name = os.getenv('MONGO_DB')
domain = os.getenv('MONGO_DOMAIN')

connect(
    host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
)


class Authors(Document):
    """Represents an author with their biographical details.

    This class is used to store information about an author, including their
    full name, date of birth, location of birth, and a brief description.

    Args:
        Document (mongoengine.Document): Inherits from MongoEngine's Document
        class to enable MongoDB document structure.

    Attributes:
        fullname (StringField): The full name of the author. This field is
            required.
        born_date (StringField): The birth date of the author as a string
            (e.g., "January 1, 1900").
        born_location (StringField): The birthplace of the author.
        description (StringField): A brief description or biography of the
            author.
    """
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    """Represents a quote associated with an author.

    This class is used to store quotes, along with the tags associated with
    the quote and a reference to the author who said or wrote it.

    Args:
        Document (mongoengine.Document): Inherits from MongoEngine's Document
            class to enable MongoDB document structure.

    Attributes:
        tags (ListField): A list of tags (keywords) associated with the quote.
        author (ReferenceField): A reference to the `Authors` document that
            identifies the author of the quote. This field is required.
        quote (StringField): The text of the quote. This field is required.
    """
    tags = ListField(StringField())
    author = ReferenceField(Authors, required=True)
    quote = StringField(required=True)


@transaction.atomic
def migrate_data(request):
    mongo_authors = Authors.objects()
    author_mapping = {}

    for mongo_author in mongo_authors:
        author, _ = Author.objects.get_or_create(name=mongo_author.fullname)
        author_mapping[str(mongo_author.id)] = author.id

    mongo_quotes = Quotes.objects()

    for mongo_quote in mongo_quotes:
        tags = []
        for tag_name in mongo_quote.tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        quote = Quote.objects.create(
            text=mongo_quote.quote,
            author_id=author_mapping[str(mongo_quote.author.id)]
        )
        quote.tags.set(tags)
        quote.save()

    print("\nMigration completed successfully!\n")
    return request
