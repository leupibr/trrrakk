from django.http import HttpResponse
from django.shortcuts import render


def login(request):
    return render(request, 'registration/login.html')


def cookie_policy(request):
    return HttpResponse("Cookie Information")


def logout(request):
    pass
