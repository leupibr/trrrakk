from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return redirect('index')


def cookie_policy(request):
    return HttpResponse("Cookie Information")

