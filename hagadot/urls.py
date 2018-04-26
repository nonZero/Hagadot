from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from books.views import HomeView, IntroView

manage_urls = [
    path('', HomeView.as_view(), name="home"),
    path('books/', include('books.urls')),
    path('text/', include('bookmarks.urls')),
    path('audio/', include('audio.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns = [
    # path('', RedirectView.as_view(url='/app/')),
    # path('', RedirectView.as_view(pattern_name='home')),
    path('', IntroView.as_view()),
    path('editors/', include(manage_urls))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
