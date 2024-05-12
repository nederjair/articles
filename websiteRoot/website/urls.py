from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls', namespace='articles')),
    path("__reload__/", include("django_browser_reload.urls")),
]
