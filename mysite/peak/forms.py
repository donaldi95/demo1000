from django import forms
from .models import Peak
from user_activities.models import Peak_annotations
from django.forms import ModelForm
import os

PEAK_STATUS = (
    ('True','Annotate'),
    ('False', 'Do not Annotate')
)


class PeakForm(forms.ModelForm):
	status = forms.ChoiceField(choices=PEAK_STATUS, widget=forms.RadioSelect())
	class Meta:
		model 	= Peak
		fields 	=['fileJson','status',]


class PeakAnnotationForm(forms.ModelForm):
	class Meta:
		model 	= 	Peak_annotations
		fields 	= 	['w_name','localized_names','valued']