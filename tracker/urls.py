from django.urls import path

from tracker import views

app_name = 'tracker'
urlpatterns = [
    path('', views.index, name='index'),

    path('<str:organization>/projects/', views.projects, name='project'),
    path('<str:organization>/projects/create', views.project_create, name='project/create'),

    path('<str:organization>/projects/<int:project_id>/details', views.project_details, name='project/details'),
    path('<str:organization>/projects/<int:project_id>/add_record', views.project_record_create, name='project/record/create'),
    path('<str:organization>/projects/<int:project_id>/edit', views.project_record_edit, name='project/record/edit'),
    path('<str:organization>/projects/<int:project_id>/delete', views.project_record_delete, name='project/record/delete'),

    path('<str:organization>/projects/<int:project_id>/timetable', views.project_timetable, name='project/timetable'),
]