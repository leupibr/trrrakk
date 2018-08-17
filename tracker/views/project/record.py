import pytz
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.datetime_safe import datetime

from tracker.forms import AddTimeRecordForm
from tracker.models import Organization, Project, Setting, TimeRecord


def create(request, organization, project_id):
    organization = get_object_or_404(Organization, name=organization)
    project = get_object_or_404(Project, id=project_id)

    setting, _ = Setting.objects.get_or_create(user=request.user)
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


def split(request, organization, project_id, record_id):
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


def edit(request, organization, project_id):
    setting, _ = Setting.objects.get_or_create(user=request.user)
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


def delete(request, organization, project_id):
    record_id = request.POST['record_id']
    entry = get_object_or_404(TimeRecord, id=record_id)

    if not entry.user == request.user:
        return HttpResponseForbidden()

    entry.delete()
    return redirect('tracker:project/timetable', organization=organization, project_id=project_id)


def start(request, organization, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not project.is_member(request.user):
        return HttpResponseForbidden()

    entry = TimeRecord(project_id=project_id, user=request.user)
    entry.start_time = datetime.now().replace(second=0, microsecond=0)
    entry.save()

    return redirect('tracker:project/timetable', organization, project_id)


def stop(request, organization, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not project.is_member(request.user):
        return HttpResponseForbidden()

    entry = get_object_or_404(TimeRecord, user=request.user, project_id=project_id, end_time=None)
    entry.end_time = datetime.now().replace(second=0, microsecond=0)
    entry.save()

    return redirect('tracker:project/timetable', organization, project_id)
