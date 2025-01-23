from django.urls import path
from . import views

urlpatterns = [
    path('', views.DialogueListView.as_view(), name='dialogue_list'),
    path('create/', views.DialogueCreateView.as_view(), name='dialogue_create'),
    path('edit/<int:pk>/', views.DialogueUpdateView.as_view(), name='dialogue_update'),
    path('delete/<int:pk>/', views.DialogueDeleteView.as_view(), name='dialogue_delete'),
    path('export/json/', views.export_json, name='export_json'),
    path('export/csv/', views.export_csv, name='export_csv'),
] 