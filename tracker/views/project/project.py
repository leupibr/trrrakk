import pytz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import activate as tz_activate
from django.utils.translation import activate as tl_activate, get_language_from_request
from django_tables2 import RequestConfig

from tracker.forms import AddTimeRecordForm
from tracker.models import Organization, Project, Setting
from tracker.tables import TimeRecordTable
from tracker.views.views import projects


@login_required
def create(request, organization):
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


@login_required
def details(request, organization, project_id):
    raise Http404()


@login_required
def timetable(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    setting, _ = Setting.objects.get_or_create(user=request.user)
    timezone = pytz.timezone(str(setting.timezone))

    tl_activate(get_language_from_request(request))
    tz_activate(timezone)

    time_records = TimeRecordTable(project.timerecord_set.all(), request=request)
    time_records.order_by = '-end_time'
    RequestConfig(request).configure(time_records)

    form_add_record = AddTimeRecordForm()

    context = dict(
        organization=organization,
        project=project,
        time_records=time_records,
        form_add_record=form_add_record
    )
    return render(request, 'tracker/timetable.html', context)