from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.BookmarkListView.as_view(), name='list'),
    path('<int:pk>/', views.BookmarkDetailView.as_view(), name='detail'),
]
