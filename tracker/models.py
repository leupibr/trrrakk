import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    admins = models.ManyToManyField(get_user_model(), related_name='administrated_organizations', verbose_name='Administrators')
    members = models.ManyToManyField(get_user_model(), blank=True, related_name='organization_memberships')

    def is_user_space(self):
        return self.name.startswith('~')
    is_user_space.boolean = True

    def is_admin(self, user):
        return user in self.admins.all()

    def is_member(self, user):
        pass

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)

    admins = models.ManyToManyField(get_user_model(), related_name='administrated_projects', verbose_name='Administrators')
    editors = models.ManyToManyField(get_user_model(), blank=True, related_name='editable_projects')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.name, self.organization.name)


class TimeRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    modification_time = models.DateTimeField(auto_now=True)

    def duration(self):
        if not self.end_time:
            return datetime.timedelta()
        return self.end_time - self.start_time


class Settings(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(null=True)

