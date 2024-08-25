"""Views for quoresapp"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from .filler import migrate_data
# pylint: disable=no-member


def main(request):
    """Displays the main page with a list of all quotes.

    This view retrieves all the quotes from the database and renders them
    on the main page of the application. It is typically used to show a
    summary or list of quotes to users.

    Args:
        request (HttpRequest): The HTTP request object. This is usually a
        GET request that is handled to retrieve and display data.

    Returns:
        HttpResponse: A response object that renders the 'index.html'
        template with all the quotes.

    Context:
        quotes (QuerySet): A queryset containing all the Quote objects
        retrieved from the database.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('', views.main, name='main')
        ```

        Access the main page at:

        ```
        /
        ```
    """
    quotes = Quote.objects.all()

    return render(request, 'quotesapp/index.html', {"quotes": quotes})

@login_required
def tag(request):
    """Handles the creation of a new tag.

    This view allows authenticated users to submit a new tag. It renders a
    form for entering tag details. If the form is submitted and valid, the
    tag is saved to the database, and the user is redirected to the main
    quotes page. If the form submission is not valid, the form is re-rendered
    with validation errors.

    Args:
        request (HttpRequest): The HTTP request object. This can be a GET request
        to render the form or a POST request to submit form data.

    Returns:
        HttpResponse: A response object that either renders the 'tag.html'
        template with the form for creating a tag or redirects to the main
        page upon successful form submission.

    Context:
        form (TagForm): The form used to submit tag details.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('tag/new/', views.tag, name='tag')
        ```

        Access the tag creation page at:

        ```
        /tag/new/
        ```
    """
    form = TagForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/tag.html', {'form': form})

@login_required
def author(request):
    """Handles the creation of a new author.

    This view allows authenticated users to submit a new author. It renders a
    form for entering author details. If the form is submitted and valid, the
    author is saved to the database, and the user is redirected to the main
    quotes page. If the form submission is not valid, the form is re-rendered
    with validation errors.

    Args:
        request (HttpRequest): The HTTP request object, which can be either
        GET or POST. If POST, it contains the form data.

    Returns:
        HttpResponse: A response object that renders the 'author.html'
        template with the form for creating an author. Redirects to the
        main page if the form is successfully submitted.

    Context:
        form (AuthorForm): The form used to submit author details.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('author/new/', views.author, name='author')
        ```

        Access the author creation page at:

        ```
        /author/new/
        ```
    """
    form = AuthorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/author.html', {'form': form})

@login_required
def quote(request):
    """Handles the creation of a new quote.

    This view allows authenticated users to submit a new quote. Users must
    select an author and one or more tags associated with the quote. If the
    author is not selected, an error message is displayed. Upon successful
    submission, the quote is saved to the database and the user is redirected
    to the main quotes page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object that renders the 'quote.html' template
        with the necessary form, author, and tag data, or redirects to the
        main page upon successful submission.

    Context:
        form (QuoteForm): The form used to submit the quote data.
        authors (QuerySet): A queryset of all authors for the selection dropdown.
        tags (QuerySet): A queryset of all tags for the selection list.
        error (str, optional): An error message indicating that the author
        must be selected if the form submission is invalid.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('quote/new/', views.quote, name='quote')
        ```

        Access the quote creation page at:

        ```
        /quote/new/
        ```
    """
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_ = form.save(commit=False)
            author_id = request.POST.get('author')
            tags_ids = request.POST.getlist('tags')

            if author_id:
                quote_.author = Author.objects.get(id=author_id)
            else:
                return render(request, 'quotesapp/quote.html', {
                    'form': form,
                    'authors': Author.objects.all(),
                    'tags': Tag.objects.all(),
                    'error': 'Author must be selected!'
                })

            quote_.save()

            for tag_id in tags_ids:
                tag_ = Tag.objects.get(id=tag_id)
                quote_.tags.add(tag_)

            return redirect('quotesapp:main')
    else:
        form = QuoteForm()

    return render(request, 'quotesapp/quote.html', {
        'form': form,
        'authors': Author.objects.all(),
        'tags': Tag.objects.all(),
    })

def author_quotes(request, author_id):
    """Displays a list of quotes attributed to a specific author.

    This view retrieves all quotes associated with a given author, identified
    by `author_id`. If the author does not exist, a 404 error is raised. The
    quotes are then displayed on a dedicated page for that author.

    Args:
        request (HttpRequest): The HTTP request object.
        author_id (int): The ID of the author whose quotes are to be displayed.

    Returns:
        HttpResponse: A response object that renders the 'author_quotes.html'
        template with the context containing the author and their quotes.

    Raises:
        Http404: If the author with the specified `author_id` does not exist.

    Context:
        author (Author): The author object corresponding to the provided `author_id`.
        quotes (QuerySet): A queryset of quotes associated with the specified author.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('authors/<int:author_id>/quotes/', views.author_quotes, name='author_quotes')
        ```

        To access quotes by a specific author:

        ```
        /authors/1/quotes/
        ```
    """
    author_ = get_object_or_404(Author, id=author_id)

    quotes = Quote.objects.filter(author=author_)

    return render(request, 'quotesapp/author_quotes.html', {
        'author': author_,
        'quotes': quotes
    })

def quotes_by_tag(request, tag_id):
    """Displays a list of quotes associated with a specific tag.

    This view retrieves all quotes that are linked to a given tag, identified by
    `tag_id`. If the tag does not exist, it raises a 404 error. The quotes
    associated with the tag are then rendered on a dedicated page.

    Args:
        request (HttpRequest): The HTTP request object.
        tag_id (int): The ID of the tag used to filter quotes.

    Returns:
        HttpResponse: A response object that renders the 'quotes_by_tag.html'
        template with the context containing the tag and associated quotes.

    Raises:
        Http404: If the tag with the specified `tag_id` does not exist.

    Context:
        tag (Tag): The tag object corresponding to the provided `tag_id`.
        quotes (QuerySet): A queryset of quotes associated with the specified tag.

    Example Usage:
        URL pattern in `urls.py`:

        ```python
        path('tags/<int:tag_id>/quotes/', views.quotes_by_tag, name='quotes_by_tag')
        ```

        To access quotes associated with a tag:

        ```
        /tags/1/quotes/
        ```
    """
    tag_ = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag_)

    return render(request, 'quotesapp/quotes_by_tag.html', {
        'tag': tag_,
        'quotes': quotes,
    })

@login_required
def migration(request):
    """Handles the migration of data from MongoDB to PostgreSQL.

    This view function triggers the data migration process by calling
    the `migrate_data` function. The migration process is only accessible
    to logged-in users due to the `@login_required` decorator. After the
    migration is completed, the user is redirected to the main page.

    Args:
        request: The HTTP request object that initiated the migration.

    Returns:
        HttpResponse: A redirect response to the main page of the application
        after the migration process completes.

    Example Usage:
        This view could be accessed via a URL configured in your `urls.py`,
        typically as an admin or maintenance task.

    Raises:
        Any exception raised by the `migrate_data` function will result in
        the migration process being halted, and appropriate error handling
        should be implemented based on your application's needs.
    """
    migrate_data(request)
    return redirect('quotesapp:main')
