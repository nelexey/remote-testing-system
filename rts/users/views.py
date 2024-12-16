from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'  # По умолчанию роль — user
            user.save()
            login(request, user)
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Авторизация пользователя
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Выход пользователя
def logout_view(request):
    logout(request)
    return redirect('home')
