from django import forms
from timezone_field import forms as tzforms

from tracker.models import Setting


class TimeRecordForm(forms.Form):
    start_date = forms.DateField(
        label='From Date',
        localize=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    start_time = forms.TimeField(
        label='From Time',
        localize=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    end_date = forms.DateField(
        label='To Date',
        localize=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_time = forms.TimeField(
        label='To Time',
        localize=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )


class SettingsForm(forms.ModelForm):
    timezone = tzforms.TimeZoneFormField(widget=forms.Select(attrs={'class': 'form-control'}))
    locale = forms.ChoiceField(choices=Setting.LOCALES, widget=forms.Select(attrs={'class': 'form-control'}))
    duration_format = forms.ChoiceField(
        choices=Setting.DURATION_FORMATS,
        widget=forms.Select(attrs={'class': 'form-control'}))
    allow_parallel_tracking = forms.TypedChoiceField(
        required=False,
        choices=[(True, 'Yes'), (False, 'No')],
        empty_value=False,
        coerce=lambda v: str(v).lower() == 'true',
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Setting
        fields = ('timezone', 'locale', 'duration_format', 'allow_parallel_tracking')
