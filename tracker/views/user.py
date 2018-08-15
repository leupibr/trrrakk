import json
from datetime import datetime, timedelta

import pytz
from django.shortcuts import render
from django.utils import formats
from django.utils.translation import activate as tl_activate, get_language_from_request

from tracker.models import TimeRecord, Project


def reports(request, from_date=None, to_date=None):
    from_date = begin_of_week(from_date)
    to_date = end_of_week(to_date)
    dates = [from_date + timedelta(d) for d in range(7)]

    time_records = TimeRecord.objects \
        .filter(user=request.user) \
        .filter(end_time__gte=from_date) \
        .filter(end_time__lt=to_date + timedelta(days=1)) \
        .select_related('project')

    projects = Project.objects.filter(id__in=time_records.values_list('project', flat=True).distinct())

    series = [{
        'name': project.name,
        'data': [get_records_by_project_date(time_records, project, d) for d in dates]
    } for project in projects]

    def fd(d):
        return formats.date_format(d, 'DATE_FORMAT')

    tl_activate(get_language_from_request(request))
    chart = {
        'chart': {'type': 'column'},
        'title': False,
        'xAxis': {'categories': [fd(d) for d in dates]},
        'yAxis': {'title': {'text': 'Hours (h)'}},
        'series': series
    }

    context = {
        'from_date': from_date,
        'to_date': to_date,
        'chart': json.dumps(chart),
    }

    return render(request, 'tracker/user/reports.html', context=context)


def get_records_by_project_date(time_records, project, date):
    weekday = date.isoweekday() + 1
    weekday = weekday if weekday != 7 else 1

    filtered_records = time_records \
        .filter(end_time__week_day=weekday) \
        .filter(project=project)

    delta = sum((r.duration() for r in filtered_records), timedelta())
    return to_hours_float(delta)


def to_hours_float(delta: timedelta):
    return (delta.total_seconds() // 60) / 60


def begin_of_week(date: datetime = None):
    date = date or datetime.now(tz=pytz.utc)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date - timedelta(days=date.weekday())


def end_of_week(date: datetime = None):
    date = begin_of_week(date)
    return date + timedelta(days=6)
