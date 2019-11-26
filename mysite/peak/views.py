from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
	ListView, 
	CreateView,
	)
from django.views.generic import FormView

from .forms import PeakForm
from campaign.models import Campaign
from .models import Peak

	
class PeakListView(ListView):
	model = Peak
	template_name = 'peak/peak.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'peak'
	ordering = ['-date_posted']