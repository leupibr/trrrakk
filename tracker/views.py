from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig

from tracker.models import Organization, Project
from tracker.tables import TimeRecordTable


def index(request):
    context = dict(recent_projects=[])
    return render(request, 'tracker/index.html', context)


def projects(request, organization, **kwargs):
    organization = Organization.get_or_create_by_name(name=organization, user=request.user)

    context = dict(
        organization=organization,
        projects=Project.objects.filter(organization=organization, admins__in=[request.user]),
        random_project_name=Project.random_name(),
        **kwargs)
    return render(request, 'tracker/projects.html', context)


def project_create(request, organization):
    organization = get_object_or_404(Organization, name=organization)

    if not organization.is_admin(request.user):
        return HttpResponseForbidden()

    try:
        project_name = request.POST['project_name']
        if not project_name.strip():
            raise KeyError()
    except KeyError:
        return projects(request, organization=organization.name, error_message="You didn't enter a project name.")

    project = Project(name=project_name, organization=organization)
    project.save()
    project.admins.add(request.user)
    project.save()

    return redirect('tracker:project', organization=organization)


def project_details(request, organization, project_id):
    raise Http404()


def project_timetable(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    time_records = TimeRecordTable(project.timerecord_set.all())
    time_records.order_by = 'end_time'
    RequestConfig(request).configure(time_records)

    context = dict(
        organization=organization,
        project=project,
        time_records=time_records
    )
    return render(request, 'tracker/timetable.html', context)


