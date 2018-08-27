from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from tracker.models import Organization


class OrganizationModelTests(TestCase):
    def test_is_userspace(self):
        subject = Organization()
        subject.name = '~username'

        self.assertIs(True, subject.is_user_space())

    def test_not_is_userspace(self):
        subject = Organization()
        subject.name = 'Organization'

        self.assertIs(False, subject.is_user_space())

    def test_is_admin(self):
        subject = Organization()
        subject.save()

        user = User()
        user.save()
        self.assertIs(False, subject.is_admin(user))
        self.assertIs(False, subject.is_member(user))

        subject.admins.add(user)
        self.assertIs(True, subject.is_admin(user))
        self.assertIs(True, subject.is_member(user))

    def test_is_member(self):
        subject = Organization()
        subject.save()

        user = User()
        user.save()
        self.assertIs(False, subject.is_member(user))

        subject.members.add(user)
        self.assertIs(True, subject.is_member(user))

    def test_get_or_create_by_name_non_existing_non_user(self):
        user = User(username='username')
        user.save()

        with self.assertRaises(Http404):
            Organization.get_or_create_by_name('MyOrganization', user)

    def test_get_or_create_by_name_non_existing_user(self):
        user = User(username='username')
        user.save()

        subject = Organization.get_or_create_by_name('~' + user.username, user)
        self.assertIsInstance(subject, Organization)
        self.assertIsNotNone(subject.id)
        self.assertIs(True, subject.is_admin(user))

    def test_get_or_create_existing(self):
        user = User(username='username')
        user.save()

        org = Organization(name='MyOrganization')
        org.save()

        subject = Organization.get_or_create_by_name('MyOrganization', user)
        self.assertIsInstance(subject, Organization)
        self.assertIsNotNone(subject.id)

    def test__str__(self):
        subject = Organization(name='MyOrganization')
        self.assertEqual('MyOrganization', str(subject))

