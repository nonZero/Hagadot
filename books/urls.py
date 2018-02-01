from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BookUpdateView.as_view(), name='update'),
    path('<int:pk>/<int:ordinal>/', views.PageDetailView.as_view(), name='page'),
    path('<int:pk>/<int:ordinal>/create-annotation/',
         views.AnnotationCreateView.as_view(), name='create_ann'),
    path('annotations/edit/<int:pk>/',
         views.AnnotationUpdateView.as_view(), name='update_ann'),
    path('annotations/delete/<int:pk>/',
         views.AnnotationDeleteView.as_view(), name='delete_ann'),
    path('annotations/edit-position/<int:pk>/',
         views.AnnotationUpdatePositionView.as_view(), name='update_ann_pos'),
]
