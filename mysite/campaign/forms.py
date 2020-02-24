from django.forms import ModelForm
from .models import Campaign
from django.core.exceptions import ValidationError
from django import forms

class Update_Campaign(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ['name', 'status', 'start_date','end_date']


class Create_campaigns(forms.ModelForm):

    def clean_status(self):
        if self.cleaned_data['status'] != 'Created':
            raise ValidationError('Status should be Created')
        return self.cleaned_data['status']
    class Meta:
        model = Campaign
        fields = ['name', 'status', 'start_date','end_date']