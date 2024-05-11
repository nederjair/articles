from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # article views
    path('', views.article_list, name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>/', views.article_detail, name='article_detail'),
]
