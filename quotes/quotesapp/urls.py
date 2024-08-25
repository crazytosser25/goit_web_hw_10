"""Url list for quotesapp"""
from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('authors/<int:author_id>/', views.author_quotes, name='author_quotes'),
    path('tags/<int:tag_id>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('migration/', views.migration, name='migration'),
]
