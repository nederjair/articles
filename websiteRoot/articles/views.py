from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Section, SectionOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def article_list(request):
    article_list = Article.objects.all()
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
    return render(request, 'articles/article/list.html', {'articles': articles})


def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article, slug=article, created__year=year, created__month=month, created__day=day)
    sections = article.sections.all()
    # List of active comments for this article

    return render(request, 'articles/article/detail.html', {'article': article, 'sections': sections})


