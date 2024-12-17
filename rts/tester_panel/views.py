from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import TestForm
from tests.models import Test
from .decorators import role_required

@role_required(['tester', 'admin'])
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            messages.success(request, "Test created successfully.")
            return redirect('tester_panel:test_list')
    else:
        form = TestForm()
    return render(request, 'tester_panel/create.html', {'form': form})

@role_required(['tester', 'admin'])
def edit_test(request, pk):
    test = get_object_or_404(Test, pk=pk, author=request.user)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            messages.success(request, "Test updated successfully.")
            return redirect('tester_panel:test_list')
    else:
        form = TestForm(instance=test)
    return render(request, 'tester_panel/edit.html', {'form': form, 'test': test})

@role_required(['tester', 'admin'])
def delete_test(request, pk):
    test = get_object_or_404(Test, pk=pk, author=request.user)
    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test deleted successfully.")
        return redirect('tester_panel:test_list')
    return render(request, 'tester_panel/delete.html', {'test': test})

@role_required(['tester', 'admin'])
def test_list(request):
    tests = Test.objects.filter(author=request.user)
    return render(request, 'tester_panel/list.html', {'tests': tests})
