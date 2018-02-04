from django.urls import path

from . import views

app_name = 'audio'

urlpatterns = [
    path('', views.TrackListView.as_view(), name='list'),
    path('import/', views.TrackImportView.as_view(), name='import'),
    path('<int:pk>/', views.TrackDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TrackUpdateView.as_view(), name='update'),
]
