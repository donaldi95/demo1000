from django import forms
from .models import Peak
from django.forms import ModelForm


class PeakForm(ModelForm):
	class Meta:
		model = Peak
		fields = ['name',]
