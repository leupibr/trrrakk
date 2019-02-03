import calendar
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
def reports(request):
    return render(request, 'tracker/user/reports.html')

@login_required
def monthly_distribution(request, from_date=None, to_date=None):
    from_date = from_date or request.GET.get('from', None)
    to_date = to_date or request.GET.get('to', None)

    setting, _ = Setting.objects.get_or_create(user=request.user)
    tl_activate(setting.locale)

    from_date = begin_of_month(from_date)
    to_date = end_of_month(to_date)
    dates = [from_date + timedelta(d) for d in range(to_date.day)]

    time_records = TimeRecord.objects \
        .filter(user=request.user) \
        .filter(end_time__gte=from_date) \
        .filter(end_time__lt=to_date + timedelta(days=1)) \
        .select_related('project')

    projects = Project.objects.filter(id__in=time_records.values_list('project', flat=True).distinct())
    print(projects)

    matrix = [{
        'project': project,
        'duration': build_sum(setting, [
            format_matrix[setting.duration_format](get_duration_by_date(time_records, project, d)) for d in dates
        ])}
        for project in projects]
    total = build_sum(setting, [p['duration'] for p in matrix])

    series = [{
        'name': entry['project'].name,
        'y': format_data[setting.duration_format](entry['duration'])
    } for entry in matrix]

    def fd(d, f='DATE_FORMAT'):
        return formats.date_format(d, f)

    try:
        title = f"{fd(from_date, 'B')} Work Distribution"
    except:
        title = f"Work Distribution {fd(from_date)} - {fd(to_date)}"

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': title},
        'plotOptions': {'pie': {
            'allowPointSelect': True,
            'cursor': 'pointer',
            'dataLabels': {'enabled': False},
            'showInLegend': True
        }},
        'series': [{'name': 'Distribution', 'data': series}]
    }

    backward_step = timedelta(days=(from_date - timedelta(days=1)).day)
    next_month_date = to_date + timedelta(days=1)
    _, forward_step = calendar.monthrange(from_date.year, from_date.month)
    _, to_forward_step = calendar.monthrange(next_month_date.year, next_month_date.month)

    context = {
        'setting': setting,
        'show_identifier': any(p.identifier for p in projects),
        'matrix': matrix,
        'total': total,
        'chart': json.dumps(chart),
        'step': {
            'backward': get_backward_step(from_date, backward_step),
            'forward': get_forward_step(from_date, timedelta(days=forward_step), timedelta(days=to_forward_step-1))
        }
    }

    return render(request, 'tracker/user/monthly_distribution.html', context=context)


@login_required
def weekly_time(request, from_date=None, to_date=None):
    from_date = from_date or request.GET.get('from', None)
    to_date = to_date or request.GET.get('to', None)

    setting, _ = Setting.objects.get_or_create(user=request.user)
    tl_activate(setting.locale)

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
            format_matrix[setting.duration_format](get_duration_by_weekday(time_records, project, d)) for d in dates
        ]}
        for project in projects]
    totals = build_sum_for_dates(setting, dates, matrix)

    series = [{
        'name': entry['project'].name,
        'data': [format_data[setting.duration_format](r) for r in entry['duration']]
    } for entry in matrix]

    def fd(d, f='DATE_FORMAT'):
        return formats.date_format(d, f)

    title = f"Report Week {fd(from_date, 'W')} ({fd(from_date)} - {fd(to_date)})"
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': title},
        'xAxis': {'categories': [fd(d) for d in dates]},
        'yAxis': {'title': {'text': 'Hours (h)'}},
        'series': series
    }

    context = {
        'setting': setting,
        'show_identifier': any(p.identifier for p in projects),
        'projects': projects,
        'dates': dates,
        'matrix': matrix,
        'totals': totals,
        'chart': json.dumps(chart),
        'step': {
            'backward': get_backward_step(from_date, timedelta(days=7)),
            'forward': get_forward_step(from_date, timedelta(days=7), timedelta(days=13))
        }
    }

    return render(request, 'tracker/user/weekly_time.html', context=context)


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


def build_sum_for_dates(setting, dates, matrix):
    init = 0 if setting.duration_format == Setting.DURATION_FORMAT_DECIMAL else timedelta()
    return [sum([p['duration'][i] for p in matrix], init) for i in range(len(dates))]


def build_sum(setting, values):
    init = 0 if setting.duration_format == Setting.DURATION_FORMAT_DECIMAL else timedelta()
    return sum(values, init)


def get_backward_step(current: datetime, step: timedelta):
    return {
        'from': (current - step).strftime('%Y-%m-%d'),
        'to': (current - timedelta(days=1)).strftime('%Y-%m-%d'),
    }


def get_forward_step(current: datetime, step: timedelta, duration: timedelta):
    return {
        'from': (current + step).strftime('%Y-%m-%d'),
        'to': (current + step + duration).strftime('%Y-%m-%d'),
    }


def get_duration_by_weekday(time_records, project, date):
    weekday = date.isoweekday() + 1
    weekday = weekday if weekday != 7 else 1

    filtered_records = time_records \
        .filter(end_time__week_day=weekday) \
        .filter(project=project)

    return sum((r.duration() for r in filtered_records), timedelta())


def get_duration_by_date(time_records, project, date):
    filtered_records = time_records \
        .filter(end_time__date=date) \
        .filter(project=project)

    return sum((r.duration() for r in filtered_records), timedelta())


def to_decimal(delta: timedelta):
    return (delta.total_seconds() // 60) / 60


format_matrix = {
    Setting.DURATION_FORMAT_CLASSIC: lambda v: v,
    Setting.DURATION_FORMAT_DECIMAL: to_decimal,
}

format_data = {
    Setting.DURATION_FORMAT_CLASSIC: to_decimal,
    Setting.DURATION_FORMAT_DECIMAL: lambda v: v,
}


def begin_of_week(date: Union[datetime, str] = None):
    date = date or datetime.now(tz=pytz.utc)
    if not isinstance(date, datetime):
        date = datetime.strptime(date, '%Y-%m-%d')

    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date - timedelta(days=date.weekday())


def begin_of_month(date: Union[datetime, str] = None):
    date = date or datetime.now(tz=pytz.utc)
    if not isinstance(date, datetime):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def end_of_week(date: Union[datetime, str] = None):
    date = begin_of_week(date)
    return date + timedelta(days=6)


def end_of_month(date: Union[datetime, str] = None):
    date = begin_of_month(date)
    weekday, day = calendar.monthrange(date.year, date.month)
    return date.replace(day=day)
