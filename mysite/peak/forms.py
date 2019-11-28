from django import forms
from .models import Peak
from django.forms import ModelForm
import os

class PeakForm(forms.ModelForm):
	class Meta:
		model = Peak
		fields =['fileJson',]