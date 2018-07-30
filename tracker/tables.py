import django_tables2 as tables

from tracker.models import TimeRecord


class TimeRecordTable(tables.Table):
    class Meta:
        model = TimeRecord
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'start_time', 'end_time', 'duration', 'action')
