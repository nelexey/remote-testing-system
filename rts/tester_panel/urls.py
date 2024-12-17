from django.urls import path
from . import views

app_name = 'tester_panel'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('create/', views.create_test, name='create_test'),
    path('edit/<int:pk>/', views.edit_test, name='edit_test'),
    path('delete/<int:pk>/', views.delete_test, name='delete_test'),
]