from django.contrib import admin

from tracker.models import Organization
from tracker.models import Project
from tracker.models import Profile
from tracker.models import TimeRecord


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('User Management', {'fields': ['admins', 'members'], 'classes': ['collapse']})
    ]

    list_display = ('name', 'is_user_space')
    search_fields = ['name']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ['user__username']


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'organization']}),
        ('User Management', {'fields': ['admins', 'editors'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'organization')
    search_fields = ['name']


class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'start_time', 'end_time', 'duration')
    list_filter = ['user', 'project']

    search_fields = ['user__username', 'project__name', 'start_time', 'end_time']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeRecord, TimeRecordAdmin)
