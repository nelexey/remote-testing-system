from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

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
    return redirect('index')

@login_required
def home(request):
    return redirect('user_profile', username=request.user.username)


def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    is_owner = request.user.is_authenticated and request.user.username == username
    context = {
        'user_profile': {
            'username': user.username,
            'email': user.email,
            'role': user.get_role_display(),
            'updated_at': user.updated_at,
        },
        'is_owner': is_owner
    }
    return render(request, 'users/profile.html', context)