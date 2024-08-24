from django.shortcuts import render, redirect
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
# pylint: disable=no-member


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})

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
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_ = form.save(commit=False)
            author_id = request.POST.get('author')
            tags_ids = request.POST.getlist('tags')

            Author.objects.get(id=author_id)
            quote_.save()

            for tag_id in tags_ids:
                Tag.objects.get(id=tag_id)
                quote_.tags.add(tag_id)

            return redirect('quotesapp:main')
    else:
        form = QuoteForm()

    authors = Author.objects.all()
    tags = Tag.objects.all()
    return render(request, 'quotesapp/quote.html', {
        'form': form,
        'authors': authors,
        'tags': tags
    })
