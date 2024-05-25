from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm

def article_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    article_list = Article.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        article_list = article_list.filter(category=category)
    # Pagination with 3 articles per page
    paginator = Paginator(article_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    return render(request, 'articles/article/list.html', {'category': category, 'categories': categories, 'articles': articles})


def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article, slug=article, created__year=year, created__month=month, created__day=day)
    sections = article.sections.all()
    context = {'article': article,
               'sections': sections,
               }
    return render(request, 'articles/article/detail.html', context)

def article_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Article.objects.annotate(search=SearchVector('title', 'description'),).filter(search=query)
    return render(request, 'articles/article/search.html', {'form': form, 'query': query, 'results': results})
