from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'core/index.html', context)