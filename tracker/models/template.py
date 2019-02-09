from django.contrib.auth.models import User
from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


