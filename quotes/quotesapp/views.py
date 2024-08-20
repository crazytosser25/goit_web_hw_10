from django.shortcuts import render, redirect
from .forms import TagForm, AuthorForm

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
