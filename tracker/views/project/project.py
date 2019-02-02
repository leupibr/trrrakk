from datetime import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import activate as tz_activate
from django.utils.translation import activate as tl_activate
from django_tables2 import RequestConfig

from tracker.forms import TimeRecordForm
from tracker.models import Organization, Project, Setting
from tracker.tables import TimeRecordTable, RecentRecordTable
from tracker.views.views import projects


@login_required
def create(request, organization):
    organization = get_object_or_404(Organization, name=organization)

    if not organization.is_admin(request.user):
        return HttpResponseForbidden()

    try:
        project_name = request.POST['project_name']
        identifier = request.POST['identifier']
        if not project_name.strip():
            raise KeyError()
    except KeyError:
        return projects(request, organization=organization.name, error_message="You didn't enter a project name.")

    project = Project(name=project_name, identifier=identifier, organization=organization)
    project.save()
    project.admins.add(request.user)
    project.save()

    return redirect('tracker:project', organization=organization)


@login_required
def delete(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    if not organization.is_admin(request.user):
        return HttpResponseForbidden()

    project.delete()
    return redirect('tracker:project', organization=organization)


@login_required
def details(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    setting, _ = Setting.objects.get_or_create(user=request.user)
    timezone = pytz.timezone(str(setting.timezone))

    if not project.is_member(request.user):
        return HttpResponseForbidden()

    tl_activate(setting.locale)
    tz_activate(timezone)

    members = set(set(project.admins.all()) | set(project.editors.all()))

    recent_query = project.timerecord_set.order_by('-end_time')[:5]
    recent_changes = RecentRecordTable(recent_query, request=request)
    RequestConfig(request, paginate=False).configure(recent_changes)

    context = dict(
        organization=organization,
        project=project,
        members=members,
        recent_changes=recent_changes
    )
    return render(request, 'tracker/project/details.html', context)


@login_required
def timetable(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    setting, _ = Setting.objects.get_or_create(user=request.user)
    timezone = pytz.timezone(str(setting.timezone))

    if not project.is_member(request.user):
        return HttpResponseForbidden()

    tl_activate(setting.locale)
    tz_activate(timezone)

    time_records = TimeRecordTable(project.timerecord_set.all(), request=request)
    request.session['timetable.sort'] = request.GET.get('sort') or request.session.get('timetable.sort')
    time_records.order_by = request.session.get('timetable.sort') or '-end_time'
    RequestConfig(request, paginate={'per_page': 15}).configure(time_records)

    form_add_record = TimeRecordForm(initial={
        "start_time": datetime.now(timezone).strftime('%Y-%m-%dT%H:%M')
    })
    form_edit_record = TimeRecordForm(initial={
        "end_time": datetime.now(timezone).strftime('%Y-%m-%dT%H:%M')
    })

    context = dict(
        organization=organization,
        project=project,
        time_records=time_records,
        form_add_record=form_add_record,
        form_edit_record=form_edit_record
    )
    return render(request, 'tracker/timetable.html', context)
