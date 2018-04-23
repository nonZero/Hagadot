from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.RowListView.as_view(), name='all'),
    path('json/', views.BookmarksAPIView.as_view(), name='json'),

    path('bookmark/', views.BookmarkListView.as_view(), name='list'),
    path('bookmark/<int:pk>/', views.BookmarkDetailView.as_view(),
         name='detail'),
]
