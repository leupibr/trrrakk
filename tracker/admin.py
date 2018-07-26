from django.contrib import admin

from tracker.models import Organization, Project, TimeRecord, Profile


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('User Management', {'fields': ['admins', 'members'], 'classes': ['collapse']})
    ]

    list_display = ('name', 'is_user_space')
    search_fields = ['name']


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'organization']}),
        ('User Management', {'fields': ['admins', 'editors'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'organization')


class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'start_time', 'end_time', 'duration')
    list_filter = ['user', 'project']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeRecord, TimeRecordAdmin)

admin.site.register(Profile)
