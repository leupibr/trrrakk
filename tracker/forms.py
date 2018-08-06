from django import forms


class AddTimeRecordForm(forms.Form):
    start_time = forms.DateTimeField(
        label='From',
        localize=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))

    end_time = forms.DateTimeField(
        label='To',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))

