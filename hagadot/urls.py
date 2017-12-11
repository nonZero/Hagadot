from django.contrib import admin
from django.urls import path, include
from books.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('books/', include('books.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('admin/', admin.site.urls),
]
