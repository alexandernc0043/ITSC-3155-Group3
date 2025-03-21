from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def login(request):
    return render(request, 'base/login.html')


def register(request):
    return render(request, 'base/register.html')


def review(request, pk):
    return render(request, 'base/review.html')
