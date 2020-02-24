from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden,HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
	ListView, 
	CreateView,
	DetailView, 
	)
from django.urls import reverse
from django.views.generic import FormView
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.views.generic.edit import FormMixin,ModelFormMixin
from .forms import PeakForm, PeakAnnotationForm
from campaign.models import Campaign
from users.models import MyUser

from user_activities.models import Peak_annotations,Campaign_enrollment
from .models import Peak
import json
import datetime 
  
class PeakListView(FormMixin,LoginRequiredMixin,ListView):
	model 				=  Peak
	template_name 		= 'peak/peak.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'peak'
	form_class	 		=  PeakAnnotationForm

	def get_context_data(self, **kwargs):
		context 				= super(PeakListView, self).get_context_data(**kwargs)
		context["form"] 		= self.get_form()
		context["user_enrolled"]= Campaign_enrollment.objects.filter(user_id = self.request.user.id)
		context["status"]       = list(Campaign.objects.filter(id=self.kwargs['pk']).values('status'))
		context["end_date"]     = Campaign.objects.filter(id=self.kwargs['pk']).values('end_date')
		context["actual_date"]  = datetime.datetime.now().strftime("%Y-%m-%d")

		peaks_campaign 			= Peak.objects.filter(campaign_id = self.kwargs['pk']).values_list('id',flat=True)
		evaluated_peaks 		= Peak_annotations.objects.filter(peak_id__in = peaks_campaign, user_id = self.request.user.id).values_list('peak_id').distinct()
		context["not_evalated_peaks"] = Peak.objects.filter(campaign_id = self.kwargs['pk'],status = 1).exclude(id__in=evaluated_peaks).values()
		context["evalated_peaks"] = Peak.objects.filter(campaign_id = self.kwargs['pk'], id__in = evaluated_peaks,status = 1).values()
		context["not_to_annotate"] = Peak.objects.filter(campaign_id = self.kwargs['pk'],status = 0).values()

		print(context["not_evalated_peaks"])
		print(context["evalated_peaks"])
		self.campaign_id 		= Campaign.objects.filter(user_id= self.request.user,id=self.kwargs['pk'])
		if self.campaign_id:
				self.campaign_id 		= get_object_or_404(Campaign, id=self.kwargs['pk'])
				context	["peak_of_user"]= Peak.objects.filter(campaign_id = self.campaign_id)
		context["actualUser"]	= self.request.user
		return context

	def get_success_url(self,*args, **kwargs):
		return reverse("peak-list", kwargs={"pk": self.kwargs['pk']})

	def get_queryset(self):
		self.campaign_id = get_object_or_404(Campaign, id=self.kwargs['pk'])
		return Peak.objects.filter(campaign_id=self.campaign_id)

	def post(self, request, pk, *args, **kwargs):
		if self.request.is_ajax():
			mydata = json.loads(request.body)
			if request.method == 'POST' and mydata['action'] == 'getPeakData':
				has_annotated = False 
				if(Peak_annotations.objects.filter(peak_id = mydata['peak_id'], user_id = self.request.user.id).values()):
					has_annotated = True
				print(has_annotated)
				peaks1 = list(Peak.objects.filter(id = mydata['peak_id']).values())
				data1  = list(Peak_annotations.objects.filter(peak_id = mydata['peak_id']).values())
				data   = {
					'peaks_json':peaks1, 
					'annotations':data1,
					'has_annotated':has_annotated,
					}
				#print(data['annotations'])
				return JsonResponse({'peaks': data},content_type='application/json')
		else:
			self.object = Peak.objects

			form = self.get_form()
			if form.data['hidden_id'] != '0':
				
				if form.is_valid():
					has_annotated = False 
					if(Peak_annotations.objects.filter(peak_id = form.data['hidden_id'], user_id = self.request.user.id).values()):
						messages.warning(request, 'You have already annotated valid')
						return HttpResponseRedirect(reverse('peak-list', kwargs={'pk':self.kwargs['pk']}))
					else:
						peak 						 = get_object_or_404(Peak, id=form.data['hidden_id'])
						user 						 = get_object_or_404(MyUser, id=self.request.user.id)
						form.instance.peak_id 		 = peak
						form.instance.user_id 		 = user
						form.instance.name 			 = form.data['w_name']
						form.instance.localize_names = form.data['localized_names']
						form.save()
						messages.warning(request, 'Your annotation is waiting for review valid')
						return HttpResponseRedirect(reverse('peak-list', kwargs={'pk':self.kwargs['pk']}))
				else:
					messages.warning(request, 'Form is not valid')
					return HttpResponseRedirect( reverse('peak-list', kwargs={'pk':self.kwargs['pk']}))
			else:
				messages.warning(request, 'You need to select an Peak to annotate')
				return HttpResponseRedirect(reverse('peak-list', kwargs={'pk':self.kwargs['pk']}))
		return  HttpResponseRedirect(reverse('peak-list', kwargs={'pk':self.kwargs['pk']}))


	#def form_valid(self,form):
		#form.fields 				 = self.object
		#return super().form_valid(form)



class PeakDetailView(LoginRequiredMixin,DetailView):
	model 		 	= Peak
	template_name 	= 'peak/peak_detail.html'

	def get_context_data(self, *args, **kwargs):
		context 						= super(PeakDetailView, self).get_context_data(*args, **kwargs)
		context['annotation_list'] 		= json.loads(json.dumps(list(Peak_annotations.objects.filter(peak_id=self.kwargs['pk']).values())))
		peak							= Peak.objects.get(id=self.kwargs['pk'])
		context['peak_lat']				= peak.lat
		context['peak_lon']				= peak.lon
		context['peak_name']			= peak.name
		return context

	#to do here is to clear the form after submit
	def post(self, request, *args, **kwargs):
		# When the form is submitted, it will enter here
		self.object 			= None
		annotation 				= Peak_annotations.objects.get(peak_id = self.kwargs['pk'])

		annotation.status 		= self.request.POST.get('evaluateAnnotation')
		#annotation.status 		= True
		#post.campaign_id	= Campaign.objects.get(id = request.POST.get('id'))
		#post.user_id   	= request.user
		annotation.save()
		# Whether the form validates or not, the view will be rendered by get()
		messages.success(request, 'You reviewd the annotaion')

		return HttpResponseRedirect(reverse('peak-detail', kwargs={'campaign_id':self.kwargs['campaign_id'],'pk': self.kwargs['pk']}))