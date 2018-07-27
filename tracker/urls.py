from django.urls import path

from tracker import views

app_name = 'tracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:organization>/projects/', views.projects, name='projects'),
    path('<str:organization>/projects/create', views.project_create, name='projects/create'),
]