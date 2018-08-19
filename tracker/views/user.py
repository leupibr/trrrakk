import json
from datetime import datetime, timedelta
from typing import Union

import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import formats
from django.utils.translation import activate as tl_activate

from tracker.forms import SettingsForm
from tracker.models import TimeRecord, Project, Setting


@login_required
def reports(request, from_date=None, to_date=None):
    setting, _ = Setting.objects.get_or_create(user=request.user)

    from_date = begin_of_week(from_date)
    to_date = end_of_week(to_date)
    dates = [from_date + timedelta(d) for d in range(7)]

    time_records = TimeRecord.objects \
        .filter(user=request.user) \
        .filter(end_time__gte=from_date) \
        .filter(end_time__lt=to_date + timedelta(days=1)) \
        .select_related('project')

    projects = Project.objects.filter(id__in=time_records.values_list('project', flat=True).distinct())

    matrix = [{
        'project': project,
        'duration': [
            get_duration(time_records, project, d) for d in dates
        ]}
        for project in projects]
    totals = [sum([p['duration'][i] for p in matrix], timedelta()) for i in range(len(dates))]

    series = [{
        'name': entry['project'].name,
        'data': [to_hours_float(r) for r in entry['duration']]
    } for entry in matrix]

    def fd(d, f='DATE_FORMAT'):
        return formats.date_format(d, f)

    tl_activate(setting.locale)

    title = f"Report Week {fd(from_date, 'W')} ({fd(from_date)} - {fd(to_date)})"
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'categories': [fd(d) for d in dates]},
        'yAxis': {'title': {'text': 'Hours (h)'}},
        'series': series
    }

    context = {
        'projects': projects,
        'dates': dates,
        'matrix': matrix,
        'totals': totals,
        'chart': json.dumps(chart),
        'step': {
            'backward': get_backward_step(from_date),
            'forward': get_forward_step(from_date)
        }
    }

    return render(request, 'tracker/user/reports.html', context=context)


@login_required
def settings(request):
    actual, _ = Setting.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=actual)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
    else:
        form = SettingsForm(instance=actual)

    return render(request, 'tracker/user/settings.html', context={'form': form})


def get_backward_step(current: datetime):
    return {
        'from': (current - timedelta(days=7)).strftime('%Y-%m-%d'),
        'to': (current - timedelta(days=1)).strftime('%Y-%m-%d'),
    }


def get_forward_step(current: datetime):
    return {
        'from': (current + timedelta(days=7)).strftime('%Y-%m-%d'),
        'to': (current + timedelta(days=13)).strftime('%Y-%m-%d'),
    }


def get_duration(time_records, project, date):
    weekday = date.isoweekday() + 1
    weekday = weekday if weekday != 7 else 1

    filtered_records = time_records \
        .filter(end_time__week_day=weekday) \
        .filter(project=project)

    return sum((r.duration() for r in filtered_records), timedelta())


def to_hours_float(delta: timedelta):
    return (delta.total_seconds() // 60) / 60


def begin_of_week(date: Union[datetime, str] = None):
    date = date or datetime.now(tz=pytz.utc)
    if not isinstance(date, datetime):
        date = datetime.strptime(date, '%Y-%m-%d')

    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date - timedelta(days=date.weekday())


def end_of_week(date: Union[datetime, str] = None):
    date = begin_of_week(date)
    return date + timedelta(days=6)
