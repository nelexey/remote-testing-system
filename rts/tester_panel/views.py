from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from tests.models import Test
from tests.forms import TestCreationForm


@login_required
def tester_panel(request):
    """Панель управления тестами для тестера"""
    if request.user.role != 'tester':
        messages.error(request, 'Доступ запрещен')
        return redirect('core:home')

    tests = Test.objects.filter(owner=request.user)
    return render(request, 'tester_panel/panel.html', {'tests': tests})


@login_required
def create_test(request, test_id=None):
    """Создание нового теста"""
    if request.user.role != 'tester':
        return redirect('core:home')

    if request.method == 'POST':
        form = TestCreationForm(request.POST, owner=request.user)
        if form.is_valid():
            test = form.save()
            # Обработка вопросов из POST-запроса
            # questions_data = process_questions_data(request.POST)  # Нужно реализовать
            # test.test = questions_data
            test.save()
            return redirect('tester_panel:tester_panel')
    else:
        form = TestCreationForm(owner=request.user)

    return render(request, 'tester_panel/create_test.html', {'form': form})


@login_required
def edit_test(request, test_id):
    """Редактирование существующего теста"""
    test = get_object_or_404(Test, id=test_id, owner=request.user)

    if request.method == 'POST':
        form = TestCreationForm(request.POST, instance=test, owner=request.user)
        if form.is_valid():
            test = form.save()
            # questions_data = process_questions_data(request.POST)
            # test.test = questions_data
            test.save()
            return redirect('tester_panel:tester_panel')
    else:
        form = TestCreationForm(instance=test, owner=request.user)

    return render(request, 'tester_panel/edit_test.html', {
        'form': form,
        'test': test
    })


@login_required
def delete_test_list(request):
    """Список тестов для удаления"""
    if request.user.role != 'tester':
        return redirect('core:home')

    tests = Test.objects.filter(owner=request.user)
    return render(request, 'tester_panel/delete_list.html', {'tests': tests})


@login_required
def delete_test(request, test_id):
    """Удаление теста"""
    if request.method == 'POST':
        test = get_object_or_404(Test, id=test_id, owner=request.user)
        test.delete()
        messages.success(request, 'Тест успешно удален')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)