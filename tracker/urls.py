from django.urls import path

import tracker.views as views

app_name = 'tracker'

projects_base = '<str:organization>/projects/'
project_base = f'{projects_base}<int:project_id>/'

urlpatterns = [
    path('', views.index, name='index'),

    path(f'{projects_base}', views.projects, name='project'),

    path(f'{projects_base}create', views.project.create, name='project/create'),
    path(f'{project_base}details', views.project.details, name='project/details'),
    path(f'{project_base}timetable', views.project.timetable, name='project/timetable'),

    path(f'{project_base}create', views.project.record.create, name='project/record/create'),
    path(f'{project_base}start', views.project.record.start, name='project/record/start'),
    path(f'{project_base}stop', views.project.record.stop, name='project/record/stop'),
    path(f'{project_base}edit', views.project.record.edit, name='project/record/edit'),
    path(f'{project_base}delete', views.project.record.delete, name='project/record/delete'),
    path(f'{project_base}split/<int:record_id>', views.project.record.split, name='project/record/split'),

]