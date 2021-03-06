import django_tables2 as tables
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.timezone import localtime

from tracker.models import TimeRecord


class UserColumn(tables.Column):
    def render(self, value):
        return format_html(f'{value.first_name} <b>{value.last_name}</b>')


class DateTimeColumn(tables.Column):
    def render(self, value):
        value = localtime(value)
        return format_html(f'<time datetime="{value.isoformat()}">'
                           f'{date_format(value, format="SHORT_DATETIME_FORMAT", use_l10n=True)}'
                           f'</time>')


class TimeRecordActionColumn(tables.TemplateColumn):
    def render(self, record, table, value, bound_column, **kwargs):
        start_time = '{:%Y-%m-%dT%H:%M}'.format(localtime(record.start_time))
        setattr(record, 'lstart_time', start_time)
        if record.end_time:
            end_time = '{:%Y-%m-%dT%H:%M}'.format(localtime(record.end_time))
            setattr(record, 'lend_time', end_time)
        return super(TimeRecordActionColumn, self).render(record, table, value, bound_column, **kwargs)


class TimeRecordTable(tables.Table):
    user = UserColumn(
        attrs={'td': {'data-label': 'User'}}
    )
    start_time = DateTimeColumn(
        verbose_name='Start',
        attrs={'td': {'data-label': 'Start'}}
    )
    end_time = DateTimeColumn(
        verbose_name='End',
        attrs={'td': {'data-label': 'End'}}
    )
    duration = tables.columns.Column(
        attrs={'td': {'data-label': 'Duration'}}
    )
    action = TimeRecordActionColumn(
        verbose_name='Action',
        template_name='tracker/timetable.row_action.html',
        attrs={'td': {'data-label': 'Action'}}
    )

    class Meta:
        model = TimeRecord
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'start_time', 'end_time', 'duration', 'action')
        attrs = {'class': 'table table-sm table-collapse-by-row'}


class RecentRecordTable(tables.Table):
    user = UserColumn(
        attrs={'td': {'data-label': 'User'}}
    )
    start_time = DateTimeColumn(
        verbose_name='Start',
        attrs={'td': {'data-label': 'Start'}}
    )
    end_time = DateTimeColumn(
        verbose_name='End',
        attrs={'td': {'data-label': 'End'}}
    )
    duration = tables.columns.Column(
        attrs={'td': {'data-label': 'Duration'}}
    )

    class Meta:
        model = TimeRecord
        orderable = False
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'start_time', 'end_time', 'duration')
        attrs = {'class': 'table table-sm table-collapse-by-row table-striped'}
