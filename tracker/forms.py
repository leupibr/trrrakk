from django import forms
from timezone_field import forms as tzforms

from tracker.models import Setting


class TimeRecordForm(forms.Form):
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
    timestamp_rounding = forms.ChoiceField(
        choices=Setting.ROUNDING_VALUES,
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Setting
        fields = ('timezone', 'locale', 'duration_format', 'timestamp_rounding', 'allow_parallel_tracking')


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               help_text='Password must be at least 8 characters long and must contain'
                                         ' at least one letter and one number')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
