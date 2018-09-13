from django import template

register = template.Library()


@register.filter
def is_tracking(project, user):
    return project.is_tracking(user)


@register.filter
def is_project_admin(project, user):
    return project.is_admin(user)
