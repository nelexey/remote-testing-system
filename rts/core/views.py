from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    # Получаем текущего пользователя
    user = request.user

    # Передаем данные в шаблон
    context = {
        'is_authenticated': user.is_authenticated,
        'username': user.username if user.is_authenticated else None,
        'role': user.role if user.is_authenticated and hasattr(user, 'role') else None,
    }
    return render(request, 'core/index.html', context)