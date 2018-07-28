from django.contrib.auth import get_user_model
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404


class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True)
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

    @classmethod
    def get_or_create_by_name(cls, name, user):
        try:
            return get_object_or_404(Organization, name=name)
        except Http404:
            user_org = '~{}'.format(user.username)
            if name != user_org:
                raise
            organization = Organization(name=user_org)
            organization.save()
            organization.admins.add(user)
            organization.save()
            return organization

