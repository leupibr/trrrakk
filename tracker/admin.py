from django.contrib import admin

from tracker.models import Organization, Setting
from tracker.models import Project
from tracker.models import Profile
from tracker.models import TimeRecord


user_search_fields = ['user__username', 'user__first_name', 'user__last_name']


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('User Management', {'fields': ['admins', 'members'], 'classes': ['collapse']})
    ]

    list_display = ('name', 'is_user_space')
    search_fields = ['name']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = user_search_fields


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'identifier', 'organization']}),
        ('User Management', {'fields': ['admins', 'editors'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'identifier', 'organization')
    search_fields = ['name', 'identifier']


class SettingAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ['user']

    search_fields = user_search_fields


class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'start_time', 'end_time', 'duration')
    list_filter = ['user', 'project']

    search_fields = user_search_fields + \
                    ['project__name', 'start_time', 'end_time']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(TimeRecord, TimeRecordAdmin)
