from django.urls import path
from . import views

app_name = 'tester_panel'

urlpatterns = [
    path('create/', views.create_test, name='create_test'),
    path('edit/<int:test_id>/', views.edit_test, name='edit_test'),
    path('delete/<int:test_id>/', views.delete_test, name='delete_test'),
]
