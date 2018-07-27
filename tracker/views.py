from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from tracker.models import Organization, Project


def index(request):
    context = dict(recent_projects=[])
    return render(request, 'tracker/index.html', context)


def projects(request, organization, **kwargs):
    organization = get_object_or_404(Organization, name=organization)

    context = dict(organization=organization, **kwargs)
    return render(request, 'tracker/projects.html', context)


def project_create(request, organization):
    organization = get_object_or_404(Organization, name=organization)

    if not organization.is_admin(request.user):
        return HttpResponseForbidden()

    try:
        project_name = request.POST['project_name']
    except KeyError:
        return HttpResponseRedirect(
            reverse('tracker:projects', dict(organization=organization),
                    dict(error_message="You didn't enter a project name."), ))

    project = Project(name=project_name, organization=organization)
    project.save()
    project.admins.add(request.user)
    project.save()

    kwargs = dict(organization=organization)
    return HttpResponseRedirect(reverse('tracker:projects', kwargs=kwargs))  # , args=(question.id,)))
