from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tracker.models import Organization, Project


def index(request):
    context = dict(recent_projects=[])
    return render(request, 'tracker/index.html', context)


@login_required
def projects(request, organization, **kwargs):
    organization = Organization.get_or_create_by_name(name=organization, user=request.user)

    context = dict(
        organization=organization,
        projects=Project.objects.filter(organization=organization, admins__in=[request.user]),
        random_project_name=Project.random_name(),
        **kwargs)
    return render(request, 'tracker/projects.html', context)