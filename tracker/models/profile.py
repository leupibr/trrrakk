from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Meta:
        app_label = "tracker"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(null=True)
