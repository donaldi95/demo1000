from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
	ListView, 
	CreateView,
	)
from django.urls import reverse
from django.views.generic import FormView
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.edit import FormMixin
from django.views.generic.edit import ModelFormMixin
from .forms import PeakForm, PeakAnnotationForm
from campaign.models import Campaign
from users.models import MyUser

from user_activities.models import Peak_annotations
from .models import Peak
import json
	
class PeakListView(FormMixin,ListView):
	model 				=  Peak
	template_name 		= 'peak/peak.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'peak'
	form_class	 		=  PeakAnnotationForm

	def get_context_data(self, **kwargs):
		context = super(PeakListView, self).get_context_data(**kwargs)
		context["form"] 		= self.get_form()
		context["actualUser"]	= self.request.user
		return context

	def get_success_url(self,*args, **kwargs):
		return reverse("peak-list", kwargs={"pk": self.kwargs['pk']})

	def get_queryset(self):
		self.campaign_id = get_object_or_404(Campaign, id=self.kwargs['pk'])
		return Peak.objects.filter(campaign_id=self.campaign_id)

	def post(self, request, pk, *args, **kwargs):
		if request.is_ajax():
			mydata = json.loads(request.body)
			#print(mydata['peak_id'])
			if request.method == 'POST' and mydata['action'] == 'getPeakData':
				print(mydata['action'])
				peaks = list(Peak.objects.filter(id = mydata['peak_id']).values())
				
				#print(peaks)

				return JsonResponse({'peaks': peaks},content_type='application/json')
		
		else:
			print('hey')
			self.object = Peak.objects
			form = self.get_form()
			if form.is_valid():
				return self.form_valid(form)
			else:
				return self.form_invalid(form)

		return JsonResponse({'message': 'it didnt work'},content_type='application/json')


	def form_valid(self,form):
		form.fields = self.object
		peak = get_object_or_404(Peak, id=form.data['hidden_id'])
		user = get_object_or_404(MyUser, id=self.request.user.id)
		print(user)
		#Peak.objects.filter(id=form.data['hidden_id'],slug__in=id["id"])
		#form.instance.name gets the name of the tag field
		form.instance.peak_id 		= peak
		form.instance.user_id 		= user
		form.instance.name 			= form.data['w_name']
		#form.save()
		return super().form_valid(form)