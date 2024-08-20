from django.shortcuts import render, redirect
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author
# pylint: disable=no-member

def main(request):
    return render(request, 'quotesapp/index.html')

def tag(request):
    form = TagForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/tag.html', {'form': form})

def author(request):
    form = AuthorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('quotesapp:main')

    return render(request, 'quotesapp/author.html', {'form': form})

def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()
            choice_authors = Author.objects.filter(name__in=request.POST.getlist('authors'))
            for autor in choice_authors.iterator():
                new_note.tags.add(autor)
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for teg in choice_tags.iterator():
                new_note.tags.add(teg)

            return redirect(to='quotesapp:main')
        else:
            return render(
                request,
                'quotesapp/quote.html',
                {
                    "authors": authors,
                    "tags": tags,
                    'form': form
                }
            )

    return render(
        request,
        'quotesapp/quote.html',
        {
            "authors": authors,
            "tags": tags,
            'form': QuoteForm()
        }
    )
