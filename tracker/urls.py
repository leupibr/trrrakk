from django.conf.urls import url
from django.urls import path

import tracker.views as views

app_name = 'tracker'

projects_base = '<str:organization>/projects/'
project_base = f'{projects_base}<int:project_id>/'
records_base = f'{project_base}records/'
record_base = f'{records_base}<int:record_id>/'

urlpatterns = [
    path('', views.index, name='index'),

    path(f'{projects_base}', views.projects, name='project'),

    path(f'{projects_base}create', views.project.create, name='project/create'),
    path(f'{project_base}delete', views.project.delete, name='project/delete'),
    path(f'{project_base}details', views.project.details, name='project/details'),
    path(f'{project_base}timetable', views.project.timetable, name='project/timetable'),

    path(f'{records_base}create', views.project.record.create, name='project/record/create'),
    path(f'{records_base}start', views.project.record.start, name='project/record/start'),
    path(f'{records_base}stop', views.project.record.stop, name='project/record/stop'),
    path(f'{record_base}edit', views.project.record.edit, name='project/record/edit'),
    path(f'{record_base}delete', views.project.record.delete, name='project/record/delete'),
    path(f'{record_base}split', views.project.record.split, name='project/record/split'),

    url(r'^user/reports'
        r'(?:/(?P<from_date>\d{4}-\d{2}-\d{2})'
        r'(?:/(?P<to_date>\d{4}-\d{2}-\d{2}))?'
        r')?$', views.user.reports, name='user/reports'),
    path('settings', views.user.settings, name='user/settings'),
]