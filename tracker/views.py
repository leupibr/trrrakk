from django.contrib.auth import BACKEND_SESSION_KEY
from django.shortcuts import render

from social_core.backends.google import GoogleOAuth2


def index(request):
    # backend = request.session[BACKEND_SESSION_KEY]
    # if backend.endswith(GoogleOAuth2.__name__):
    #     print(request.user)
    return render(request, 'tracker/index.html')

