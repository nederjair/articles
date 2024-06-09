from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Section, SectionOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    sections = article.sections.all()
    section_orders = []
    for section in sections:
        section_orders.append(get_object_or_404(SectionOrder, article=article, section=section))
    return render(request, 'admin/articles/article/detail.html', {'article': article, 'sections':sections, 'section_orders': section_orders})
@login_required
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


@login_required
def article_detail(request, year, month, day, article):
    categories = Category.objects.all()
    article = get_object_or_404(Article, slug=article, created__year=year, created__month=month, created__day=day)
    sections_order = SectionOrder.objects.filter(article=article).order_by('order')
    #sections = sections.order_by('section_order__order')
    #sections_info = []
    #for section in sections:
    #    sectionorder = get_object_or_404(SectionOrder, article=article, section=section)
    #    sections_info.append([sectionorder, section])
    context = {'article': article,
               #'sections': sections_info,
               'sections_order': sections_order,
               'categories': categories,
               }
    return render(request, 'articles/article/detail.html', context)

@login_required
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
