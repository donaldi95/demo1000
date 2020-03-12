from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from users.models import MyUser,Profile


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = MyUser
		fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']