from django import template

register = template.Library()


@register.filter
def is_tracking(project, user):
    return project.is_tracking(user)
