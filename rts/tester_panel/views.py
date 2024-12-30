from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from tests.models import Test
from tests.forms import TestCreationForm
import json


@login_required
def tester_panel(request):
    if request.user.role != 'tester':
        messages.error(request, 'Доступ запрещен')
        return redirect('core:home')

    tests = Test.objects.filter(owner=request.user)
    return render(request, 'tester_panel/panel.html', {'tests': tests})


@login_required
def create_test(request, test_id=None):
    if request.user.role != 'tester':
        messages.error(request, 'Доступ запрещен')
        return redirect('core:home')

    if request.method == 'POST':
        form = TestCreationForm(request.POST, owner=request.user)
        test_json = request.POST.get('test_json', '{}')
        try:
            test_data = json.loads(test_json)
        except json.JSONDecodeError:
            messages.error(request, 'Ошибка в структуре данных теста')
            return render(request, 'tester_panel/create_test.html', {'form': form})

        if not test_data.get('questions') or not isinstance(test_data.get('questions'), list):
            messages.error(request, 'Тест должен содержать хотя бы один вопрос')
            return render(request, 'tester_panel/create_test.html', {'form': form})

        if form.is_valid():
            test = form.save(commit=False)
            test.test = test_data
            test.save()
            messages.success(request, 'Тест успешно создан')
            return redirect('tester_panel:tester_panel')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = TestCreationForm(owner=request.user)

    return render(request, 'tester_panel/create_test.html', {'form': form})

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, owner=request.user)

    if request.method == 'POST':
        form = TestCreationForm(request.POST, instance=test, owner=request.user)
        if form.is_valid():
            test = form.save(commit=False)

            try:
                test_data = json.loads(request.POST.get('test_json', '{}'))

                if not test_data.get('questions'):
                    messages.error(request, 'Тест должен содержать хотя бы один вопрос')
                    return render(request, 'tester_panel/edit_test.html', {
                        'form': form,
                        'test': test
                    })


                for question in test_data['questions']:
                    # if not all(key in question for key in ['text', 'type', 'points']):
                    if not all(key in question for key in ['text', 'type']):
                        messages.error(request, 'Некорректная структура вопросов')
                        return render(request, 'tester_panel/edit_test.html', {
                            'form': form,
                            'test': test
                        })

                    if question['type'] in ['radio', 'checkbox']:
                        if not question.get('variants') or not question.get('correct'):
                            messages.error(request, 'Не указаны варианты ответов или правильный ответ')
                            return render(request, 'tester_panel/edit_test.html', {
                                'form': form,
                                'test': test
                            })

                test.test = test_data
                test.save()

                messages.success(request, 'Тест успешно обновлен')
                return redirect('tester_panel:tester_panel')

            except json.JSONDecodeError:
                messages.error(request, 'Ошибка в структуре данных теста')
                return render(request, 'tester_panel/edit_test.html', {
                    'form': form,
                    'test': test
                })
    else:
        form = TestCreationForm(instance=test, owner=request.user)

    return render(request, 'tester_panel/edit_test.html', {
        'form': form,
        'test': test
    })


@login_required
def delete_test_list(request):
    if request.user.role != 'tester':
        messages.error(request, 'Доступ запрещен')
        return redirect('core:home')

    tests = Test.objects.filter(owner=request.user)
    return render(request, 'tester_panel/delete_list.html', {'tests': tests})


@login_required
def delete_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, id=test_id, owner=request.user)

        try:
            test.delete()
            messages.success(request, 'Тест успешно удален')
            # return JsonResponse({'status': 'success'})
            return redirect('tester_panel:delete_test_list')
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Метод не разрешен'}, status=405)


@login_required
def get_test_json(request, test_id):
    test = get_object_or_404(Test, id=test_id, owner=request.user)
    return JsonResponse(test.test)