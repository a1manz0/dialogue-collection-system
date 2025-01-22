from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('edit/<int:pk>/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question_delete'),  # новый URL    
] 