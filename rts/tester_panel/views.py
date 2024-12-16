from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from tests.models import Test

# Проверка роли пользователя
def is_tester(user):
    return user.is_authenticated and (user.role == 'tester' or user.is_superuser)

@user_passes_test(is_tester)
def create_test(request):
    if request.method == 'POST':
        # Логика создания теста
        name = request.POST.get('name')
        description = request.POST.get('description')
        test = Test.objects.create(name=name, description=description, creator=request.user)
        return redirect('tester_panel:create_test')
    return render(request, 'tester_panel/create.html')

@user_passes_test(is_tester)
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, creator=request.user)
    if request.method == 'POST':
        test.name = request.POST.get('name')
        test.description = request.POST.get('description')
        test.save()
        return redirect('tester_panel:create_test')
    return render(request, 'tester_panel/edit.html', {'test': test})

@user_passes_test(is_tester)
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, creator=request.user)
    test.delete()
    return redirect('tester_panel:create_test')
