from os import path

import markdown2
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def login(request):
    if request.user.is_authenticated:
        return redirect('logout')

    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            context['error_message'] = 'Invalid username or password'

    return render(request, 'trrrakk/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('login')


def contact(request):
    return render(request, 'trrrakk/contact.html')


def cookie_policy(request):
    return render(request, 'trrrakk/policy.html')


def release_notes(request):
    html = markdown2.markdown_path(path=path.join(path.dirname(__file__), '..', 'RELEASE_NOTES.md'))
    return render(request, 'trrrakk/release_notes.html', context={'release_notes': html})
