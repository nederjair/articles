from django.contrib import admin
from .models import Article, Section, SectionOrder, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'created', 'slug']
    list_filter = ['created']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['sections']
    date_hierarchy = 'created'
    ordering = ['order']


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
