from django.contrib import admin
from .models import Article, Section, SectionOrder, Category, Subsection
from django.urls import reverse

#-----------Category Registration------------------#
class ArticleInlineAdmin(admin.TabularInline):
    fields = ['title', 'order']
    model = Article
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ArticleInlineAdmin,)

#-----------Article Registration------------------#
class SectionOrderInlineAdmin(admin.TabularInline):
    fields = ['section', 'order']
    model = Article.sections.through
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','order', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category']
    inlines = (SectionOrderInlineAdmin,)

#-----------Section Registration------------------#
class SubsectionOrderInlineAdmin(admin.TabularInline):
    fields = ['subsection', 'order']
    model = Section.subsections.through
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}
    inlines = (SubsectionOrderInlineAdmin,)
#-----------Subsection Registration------------------#
@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)}
