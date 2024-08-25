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
    """Migrates data from MongoDB collections to the corresponding PostgreSQL models.

    This function is designed to be used within a Django project to transfer
    data from MongoDB to PostgreSQL. The data includes authors, quotes, and tags.
    The function ensures that all operations are performed atomically, meaning
    either all of the data is transferred successfully, or none of it is,
    preventing partial migrations in case of an error.

    Args:
        request: The HTTP request object that initiated this migration.

    Returns:
        request: The original HTTP request object.

    The function performs the following steps:

    1. **Authors Migration**:
        - Fetches all authors from MongoDB.
        - Creates or retrieves corresponding `Author` objects in PostgreSQL.
        - Maps the MongoDB author IDs to the corresponding PostgreSQL IDs for
            linking quotes later.

    2. **Quotes Migration**:
        - Fetches all quotes from MongoDB.
        - For each quote, retrieves or creates the associated tags in PostgreSQL.
        - Creates a new `Quote` object in PostgreSQL, associates it with the
            appropriate author using the `author_mapping`, and sets the related tags.

    The `@transaction.atomic` decorator ensures that all database operations
    are wrapped in a single transaction. If any error occurs during the migration,
    all changes are rolled back to maintain database consistency.

    Example Usage:
        This function can be triggered by a Django view to start the migration
        process when needed, typically for administrative purposes.

    Raises:
        Exception: If there is any error during the migration, it will trigger
        a rollback of all database operations performed in this function.
    """
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

    return request
