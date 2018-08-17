from django import forms
from timezone_field import forms as tzforms

from tracker.models import Setting


class AddTimeRecordForm(forms.Form):
    start_time = forms.DateTimeField(
        label='From',
        localize=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))

    end_time = forms.DateTimeField(
        label='To',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))


class SettingsForm(forms.ModelForm):
    timezone = tzforms.TimeZoneFormField(widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Setting
        fields = ('timezone',)
