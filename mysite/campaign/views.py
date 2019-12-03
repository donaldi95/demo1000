from django.http import HttpResponseForbidden,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render,get_object_or_404
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView,
	)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic.edit import ModelFormMixin
from .models import Campaign
from users.models import MyUser
from peak.models import Peak
from django.contrib import messages
from peak.forms import PeakForm
from user_activities.forms import CampaignEnroll
from user_activities.models import Campaign_enrollment
import json


# Create your views here.

#this will be the home page for one campaign to check the progress
#peaks etc, this can bee seen only by admin of each campaign


### TO DO :
	# 1) MAKE THIS ACCESIBLE ONLY TO LOGGIN USERS
	# 2) SHOW HERE THE CLICKED POST

def campaign(request):
	context = {
        'campaign': Campaign.objects.all()
    }
	return render(request,'campaign/campaign.html',context)


# class base view
class CampaignListView(ListView):
	model 				= Campaign
	template_name 		= 'campaign/campaign.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'campaign'
	ordering 			= ['-date_posted']


	#to do here is to clear the form after submit
	def post(self, request, *args, **kwargs):
		# When the form is submitted, it will enter here
		self.object 		= None
		post 				= Campaign_enrollment()

		#get the campaign enrollment user ids
		user_enrolled 		= Campaign_enrollment.objects.filter(user_id = request.user)
		user_enrolled_to 	= Campaign_enrollment.objects.filter(campaign_id = request.POST.get('id'))
		if user_enrolled_to and user_enrolled:
			print("is enrollment")
			return self.get(request, *args, **kwargs)
		else:
			print("is not enrollment")
			post.campaign_id	= Campaign.objects.get(id = request.POST.get('id'))
			post.user_id   		= request.user
			post.save()
			# Whether the form validates or not, the view will be rendered by get()
			messages.success(request, 'You have Enrolled')
			return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': request.POST.get('id')}))
# a view for individual campaign
# here i am sticking to django default template just to show the difference
class CampaignDetailView(LoginRequiredMixin,UserPassesTestMixin,FormMixin,DetailView):
	model 		 = Campaign
	form_class 	 = PeakForm

	def get_success_url(self):
		return reverse("peak-list", kwargs={"pk": self.object.id})

	def get_context_data(self, **kwargs):
		context = super(CampaignDetailView, self).get_context_data(**kwargs)
		context["form"] = self.get_form()
		context["actualUser"] = self.request.user
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):
		form.fields = self.object
		#form.instance.name gets the name of the tag field
		mydata 		= form.instance.fileJson
		mydataTemp	= json.load(mydata)
		mydataTemp 	= json.dumps(mydataTemp)
		mydata3 	= json.loads(mydataTemp)

		#status of the uploaded peak
		status 		= form.instance.status
		#print("heeey")
		#print(mydata3) 
		for data in mydata3:
			print(data['provenance'])
			print(data['id'])
			#self.object gets here the Entity we are viweing

			form.instance.id 				= data['id']
			form.instance.lat 				= data['latitude']
			form.instance.lon				= data['longitude']
			form.instance.alt				= data['elevation']
			form.instance.localize_names 	= 'Null'
			form.instance.provenance_org 	= data['provenance']
			form.instance.name 				= data['name']
			form.instance.campaign_id 		= self.object
			form.instance.status 			= status
			form.save()
		return super().form_valid(form)


	def test_func(self):
		# getting the campaign that we are currently trying to update
		campaign = self.get_object()
		#the first parametter gets the  user
		if self.request.user == campaign.user_id:
			return True
		return False

	def test_func(self):
		# getting the campaign that we are currently trying to update
		#the first parametter gets the  user
		if self.request.user.is_manager == True:
			return True
		return False


# creatign a new campaign
class CampaignCreateView(UserPassesTestMixin,LoginRequiredMixin,CreateView):
	model = Campaign
	# passing the field for the form for each campaign
	fields = ['name','status','start_date','end_date']

	#checking if form is valid and we add the current user to the form
	def form_valid(self,form):
		#user_id is the id of the user we want to associate to the campaign
		form.instance.user_id = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# getting the campaign that we are currently trying to update
		#the first parametter gets the  user
		if self.request.user.is_manager == True:
			return True
		return False

# creatign a new campaign
class CampaignUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
	model = Campaign
	# passing the field for the form for each campaign
	fields = ['name','status','start_date','end_date']

	#checking if form is valid and we add the current user to the form
	def form_valid(self,form):
		#user_id is the id of the user we want to associate to the campaign
		form.instance.user_id = self.request.user
		return super().form_valid(form)

	def test_func(self):
		# getting the campaign that we are currently trying to update
		campaign = self.get_object()
		#the first parametter gets the  user
		if self.request.user == campaign.user_id:
			return True
		return False

	def test_func(self):
		# getting the campaign that we are currently trying to update
		#the first parametter gets the  user
		if self.request.user.is_manager == True:
			return True
		return False

class CampaignDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Campaign
	success_url = '/profile/'

	def test_func(self):
		# getting the campaign that we are currently trying to update
		campaign = self.get_object()
		#the first parametter gets the  user
		if self.request.user == campaign.user_id:
			return True
		return False

	def test_func(self):
		# getting the campaign that we are currently trying to update
		#the first parametter gets the  user
		if self.request.user.is_manager == True:
			return True
		return False