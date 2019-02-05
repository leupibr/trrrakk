import requests
from django.core.files.base import ContentFile
from social_core.backends.google import GoogleOAuth2

from tracker.models import Profile


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile()
        profile.user = user

    if profile.avatar:
        return

    if isinstance(backend, GoogleOAuth2):
        if not response.get('image') and response['image'].get('url'):
            return
        url = response['image'].get('url')
        ext = url.split('.')[-1].split('?')[0]
        profile.avatar.save('{0}.{1}'.format('avatar', ext), ContentFile(requests.get(url).content), save=False)
        profile.save()
