from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import ToggleCompleteView
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    RegisterView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('add/', TaskCreateView.as_view(), name='add_task'),
    path('edit/<int:pk>/', TaskUpdateView.as_view(), name='edit_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('toggle/<int:pk>/', ToggleCompleteView.as_view(), name='toggle_task'),
]