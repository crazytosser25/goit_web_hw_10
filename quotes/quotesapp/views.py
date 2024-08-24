from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

@login_required
def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_ = form.save(commit=False)
            author_id = request.POST.get('author')
            tags_ids = request.POST.getlist('tags')

            if author_id:
                quote_.author = Author.objects.get(id=author_id)
            else:
                return render(request, 'quotesapp/quote_form.html', {
                    'form': form,
                    'authors': Author.objects.all(),
                    'tags': Tag.objects.all(),
                    'error': 'Author must be selected!'
                })

            quote_.save()

            for tag_id in tags_ids:
                tag = Tag.objects.get(id=tag_id)
                quote_.tags.add(tag)

            return redirect('quotesapp:main')
    else:
        form = QuoteForm()

    return render(request, 'quotesapp/quote.html', {
        'form': form,
        'authors': Author.objects.all(),
        'tags': Tag.objects.all(),
    })
