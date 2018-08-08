import pytz
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.utils.timezone import activate as tz_activate
from django.utils.translation import activate as tl_activate
from django.utils.translation import get_language_from_request
from django_tables2 import RequestConfig

from tracker.forms import AddTimeRecordForm
from tracker.models import Organization, Project, Setting, TimeRecord
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


def project_record_create(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)
    setting = get_object_or_404(Setting, user=request.user)
    timezone = pytz.timezone(str(setting.timezone))

    if not project.is_member(request.user):
        return HttpResponseForbidden()

    entry = TimeRecord(project=project, user=request.user)
    form = AddTimeRecordForm(request.POST)

    start_time = datetime.strptime(form.data['start_time'], "%Y-%m-%dT%H:%M")
    entry.start_time = timezone.localize(start_time, is_dst=None)

    if form.data['end_time']:
        end_time = datetime.strptime(form.data['end_time'], "%Y-%m-%dT%H:%M")
        entry.end_time = timezone.localize(end_time, is_dst=None)

    entry.save()
    return redirect('tracker:project/timetable', organization=organization, project_id=project_id)


def project_record_split(request, organization, project_id, record_id):
    entry = get_object_or_404(TimeRecord, id=record_id)

    if not entry.user == request.user:
        return HttpResponseForbidden()

    entry2 = TimeRecord(user=entry.user, project=entry.project)
    entry2.end_time = entry.end_time

    duration = (entry.end_time - entry.start_time) // 2
    entry.end_time = entry.end_time - duration
    entry.end_time.replace(second=0)
    entry2.start_time = entry.end_time

    entry.save()
    entry2.save()
    return redirect('tracker:project/timetable', organization=organization, project_id=project_id)



def project_record_edit(request, organization, project_id):
    setting = get_object_or_404(Setting, user=request.user)
    timezone = pytz.timezone(str(setting.timezone))

    record_id = request.POST['record_id']
    entry = get_object_or_404(TimeRecord, id=record_id)

    if not entry.user == request.user:
        return HttpResponseForbidden()

    form = AddTimeRecordForm(request.POST)

    start_time = datetime.strptime(form.data['start_time'], "%Y-%m-%dT%H:%M")
    entry.start_time = timezone.localize(start_time, is_dst=None)

    if form.data['end_time']:
        end_time = datetime.strptime(form.data['end_time'], "%Y-%m-%dT%H:%M")
        entry.end_time = timezone.localize(end_time, is_dst=None)
    else:
        entry.end_time = None

    entry.save()
    return redirect('tracker:project/timetable', organization=organization, project_id=project_id)


def project_record_delete(request, organization, project_id):
    record_id = request.POST['record_id']
    entry = get_object_or_404(TimeRecord, id=record_id)

    if not entry.user == request.user:
        return HttpResponseForbidden()

    entry.delete()
    return redirect('tracker:project/timetable', organization=organization, project_id=project_id)


def project_timetable(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)
    setting = get_object_or_404(Setting, user=request.user)
    timezone = pytz.timezone(str(setting.timezone))
    request.session['django_timezone'] = str(setting.timezone)

    tl_activate(get_language_from_request(request))
    tz_activate(timezone)

    time_records = TimeRecordTable(project.timerecord_set.all(), request=request)
    time_records.order_by = '-end_time'
    RequestConfig(request).configure(time_records)

    form_add_record = AddTimeRecordForm()
    form_add_record.fields['start_time'].clean('2015-06-04 13:00')

    context = dict(
        organization=organization,
        project=project,
        time_records=time_records,
        form_add_record=form_add_record
    )
    return render(request, 'tracker/timetable.html', context)


