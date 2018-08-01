import django_tables2 as tables
from django.contrib.auth.models import User
from django.utils.html import format_html

from tracker.models import TimeRecord


class UserColumn(tables.Column):
    def render(self, value):
        return format_html(f'{value.first_name} <b>{value.last_name}</b>')


class DateTimeColumn(tables.Column):
    def render(self, value):
        return format_html(f'<time class="locale" datetime="{value.isoformat()}" format="lll"/>')


class TimeRecordTable(tables.Table):
    user = UserColumn()
    start_time = DateTimeColumn(verbose_name='Start')
    end_time = DateTimeColumn(verbose_name='End')

    class Meta:
        model = TimeRecord
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'start_time', 'end_time', 'duration', 'action')
