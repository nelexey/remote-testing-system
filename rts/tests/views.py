from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Test


@login_required
def create_test(request):
    if request.user.role != 'tester':  # Проверяем роль
        return HttpResponseForbidden("У вас нет прав на создание тестов.")

    if request.method == 'POST':
        # Логика создания теста
        pass

    return render(request, 'tests/create_test.html')
