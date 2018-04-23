from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from books.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('books/', include('books.urls')),
    path('text/', include('bookmarks.urls')),
    path('audio/', include('audio.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
