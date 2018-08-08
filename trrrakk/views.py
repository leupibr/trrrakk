from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def login(request):
    return render(request, 'trrrakk/login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def cookie_policy(request):
    return render(request, 'trrrakk/policy.html')

