import django_tables2 as tables
from django.utils.formats import date_format
from django.utils.html import format_html

from tracker.models import TimeRecord


class UserColumn(tables.Column):
    def render(self, value):
        return format_html(f'{value.first_name} <b>{value.last_name}</b>')


class DateTimeColumn(tables.Column):
    def render(self, value):
        return format_html(f'<time datetime="{value.isoformat()}">'
                           f'{date_format(value, format="SHORT_DATETIME_FORMAT", use_l10n=True)}'
                           f'</time>')


class TimeRecordTable(tables.Table):
    user = UserColumn()
    start_time = DateTimeColumn(verbose_name='Start')
    end_time = DateTimeColumn(verbose_name='End')

    class Meta:
        model = TimeRecord
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'start_time', 'end_time', 'duration', 'action')
