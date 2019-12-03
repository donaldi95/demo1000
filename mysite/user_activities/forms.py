from django import forms
from .models import Campaign_enrollment
from django.forms import ModelForm
import os


class CampaignEnroll(forms.ModelForm):
    hidden_field = forms.CharField(widget=forms.HiddenInput())

    class Meta:
    	model 	= Campaign_enrollment
    	fields 	= ['campaign_id',]