from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Test, TestStatistics
from django.db.models import Q


def test_list(request):
    """Страница со списком всех опубликованных тестов"""
    tests = Test.objects.filter(is_published=True).select_related('owner')

    # Фильтрация и поиск
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')

    if category:
        tests = tests.filter(category=category)
    if difficulty:
        tests = tests.filter(difficulty=difficulty)
    if search:
        tests = tests.filter(Q(title__icontains=search) | Q(description__icontains=search))

    return render(request, 'tests/test_list.html', {'tests': tests})


def test_detail(request, test_id):
    """Страница отдельного теста"""
    test = get_object_or_404(Test, id=test_id, is_published=True)
    if request.user.is_authenticated:
        attempts = TestStatistics.objects.filter(user=request.user, test=test)
        attempts_left = test.attempts_allowed - attempts.count()
    else:
        attempts = None
        attempts_left = test.attempts_allowed

    context = {
        'test': test,
        'attempts': attempts,
        'attempts_left': attempts_left
    }
    return render(request, 'tests/test_detail.html', context)


@login_required
def test_attempt(request, test_id, attempt):
    """Страница прохождения теста"""
    test = get_object_or_404(Test, id=test_id, is_published=True)

    # Проверка количества попыток
    attempts = TestStatistics.objects.filter(user=request.user, test=test).count()
    if attempts >= test.attempts_allowed:
        messages.error(request, 'Превышено максимальное количество попыток')
        return redirect('test_detail', test_id=test_id)

    if request.method == 'POST':
        # Обработка ответов на тест
        answers = request.POST.dict()
        # result = calculate_test_result(test, answers)  # Нужно реализовать эту функцию

        # Сохранение результатов
        TestStatistics.objects.create(
            user=request.user,
            test=test,
            result=result['score'],
            max_result=result['max_score'],
            time_spent=result['time_spent'],
            passed=result['passed'],
            attempt_number=attempts + 1
        )
        return redirect('test_detail', test_id=test_id)

    context = {
        'test': test,
        'attempt_number': attempts + 1
    }
    return render(request, 'tests/test_attempt.html', context)