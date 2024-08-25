"""_summary_

Returns:
    _type_: _description_
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from .filler import migrate_data
# pylint: disable=no-member


def main(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    quotes = Quote.objects.all()

    return render(request, 'quotesapp/index.html', {"quotes": quotes})

@login_required
def tag(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form = TagForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/tag.html', {'form': form})

@login_required
def author(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    form = AuthorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/author.html', {'form': form})

@login_required
def quote(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
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
    """_summary_

    Args:
        request (_type_): _description_
        author_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    author_ = get_object_or_404(Author, id=author_id)

    quotes = Quote.objects.filter(author=author_)

    return render(request, 'quotesapp/author_quotes.html', {
        'author': author_,
        'quotes': quotes
    })

def quotes_by_tag(request, tag_id):
    """_summary_

    Args:
        request (_type_): _description_
        tag_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    tag_ = get_object_or_404(Tag, id=tag_id)
    quotes = Quote.objects.filter(tags=tag_)

    return render(request, 'quotesapp/quotes_by_tag.html', {
        'tag': tag_,
        'quotes': quotes,
    })

@login_required
def migration(request):
    migrate_data(request)
    return redirect('quotesapp:main')
