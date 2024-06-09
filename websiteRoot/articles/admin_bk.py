from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article, Section, SectionOrder, Category
from django.urls import reverse

def article_detail(obj):
    url = reverse('articles:admin_article_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

class ArticleInlineAdmin(admin.TabularInline):
    fieldsets = (
        ('Article info',{
            #'classes':('collapse',),
            'fields': ('title', 'order')
        }),
    )
    model = Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ArticleInlineAdmin,)

class SectionInlineAdmin(admin.StackedInline):
    list_display = [ 'section', 'article', 'order']
    list_filter = ['article', 'section']
    search_fields  = ['article', 'section']
    ordering = ['article']
    model = Article.sections.through

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #list_display = ['title',]
    #list_filter = ['category']
    #search_fields = ['title', 'description']
    #prepopulated_fields = {'slug': ('title',)}
    #raw_id_fields = ['sections']
    #date_hierarchy = 'created'
    #ordering = ['order']
    #fieldsets = (
    #    (
    #            'Article info', {'fields': ('title',)}
    #    ),
    #)
    inlines = (SectionInlineAdmin,)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'created', 'slug']
    list_filter = ['created']
    search_fields = ['title', 'bodytext']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['created']

@admin.register(SectionOrder)
class SectionOrderAdmin(admin.ModelAdmin):
    list_display = [ 'section', 'article', 'order']
    list_filter = ['article', 'section']
    search_fields  = ['article', 'section']
    raw_id_fields = ['article', 'section']
    ordering = ['article']
