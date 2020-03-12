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
from django.http import JsonResponse

from user_activities.forms import CampaignEnroll
from django import template
from user_activities.models import Campaign_enrollment,Peak_annotations
import json
from django.http import Http404
import datetime 
from .forms import Update_Campaign,Create_campaigns

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


# class base viewd
class CampaignListView(ListView):
	model 								= Campaign
	template_name 						= 'campaign/campaign.html' # <app>/<model>_<viewtype>.html
	context_object_name 				= 'campaign'
	ordering 							= ['-date_posted']

	# making a queryset so on the campaign page will not be shown the campaigns the user has already enrolled
	def get_queryset(self):
		actualUser_enrolledTo = list(Campaign_enrollment.objects.filter(user_id = self.request.user.id).values())
		enrolledTo 			  = Campaign_enrollment.objects.filter(user_id = self.request.user.id)
		campaigns = Campaign.objects.exclude( id__in  = [x['campaign_id_id'] for x in actualUser_enrolledTo])
		return campaigns

	def get_context_data(self, **kwargs):
		#print(campaigns)
		context 						= super(CampaignListView, self).get_context_data(**kwargs)
		context["actualUser"] 			= self.request.user
		context["userHasEnrolled"]		= CheckUserEnroll(self.request.GET.get('id'), self.request.user.id)
		context["closed_campaigns"] 	= Campaign.objects.filter(status = 'Closed')
		context["actual_date"]  		= datetime.datetime.now().strftime("%Y-%m-%d")

		return context

	#to do here is to clear the form after submit
	def post(self, request, *args, **kwargs):
		# When the form is submitted, it will enter here
		self.object 					= None
		post 							= Campaign_enrollment()

		#get the campaign enrollment user ids
		#user_enrolled 		= CheckUserEnroll(request.user)
		user_enrolled_to 				= CheckUserEnroll(request.POST.get('id'), request.user )
		if user_enrolled_to:
			#print("is enrollment")
			messages.warning(request, 'You are already Enrolled')
			return HttpResponseRedirect(reverse('campaign-home'))
		else:
			#print("is not enrollment")
			post.campaign_id			= Campaign.objects.get(id = request.POST.get('id'))
			post.user_id   				= request.user
			post.save()
			# Whether the form validates or not, the view will be rendered by get()
			messages.success(request, 'You have Enrolled')
			return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': request.POST.get('id')}))


# a view for individual campaign
# here i am sticking to django default template just to show the difference
class CampaignDetailView(UserPassesTestMixin,LoginRequiredMixin,FormMixin,DetailView):
	model 		 = Campaign
	form_class 	 = PeakForm

	def get_success_url(self):
		return reverse("peak-list", kwargs={"pk": self.object.id})

	def get_context_data(self, **kwargs):
		context 						= super(CampaignDetailView, self).get_context_data(**kwargs)
		context["form"] 				= self.get_form()
		context["actualUser"] 			= self.request.user
		context["userHasEnrolled"]		= CheckUserEnroll(self.object.id, self.request.user.id)
		peak_ids						= Peak.objects.filter(campaign_id = self.kwargs['pk'], status=1).values_list('id', flat=True)
		context["peaks_notannotate"] 	= Peak.objects.filter(campaign_id = self.kwargs['pk'], status=0).values()
		peaks							= Peak.objects.filter(campaign_id = self.kwargs['pk'], status=1).values()
		context["totalPeaksForCampaign"]= peaks.count()
		annotatedPeaks = []
		rejectedPeaks  = []
		new_annotations  = []
		allPeaks 	   = 0
		#find the total non annotated peaks
		peaks = list(peaks)
		incr = 0
		annotated_peaks = None
		rejected_peaks  = None 
		peaks
		if peaks:
			#here we get all the annotations that the peaks of the campaigns have annotations
			annotated_peaks  = Peak_annotations.objects.filter(peak_id__in = peak_ids).values_list('peak_id').distinct()
			rejected_peaks   = Peak_annotations.objects.filter(peak_id__in = peak_ids,status=0).values('peak_id').distinct()
			for peak in peaks:
				temp  = Peak_annotations.objects.filter(peak_id = peak['id']).values('peak_id').distinct()
				temp2 = list(Peak_annotations.objects.filter(peak_id = peak['id'],status=0).values('peak_id').distinct())
				temp3 = list(Peak_annotations.objects.filter(peak_id = peak['id']).values())
				temp4 = Peak_annotations.objects.filter(peak_id = peak['id'],status ='').values('peak_id').distinct()
				#get all the peaks
				
				if temp:
					annotatedPeaks.append(temp)

				if temp2:
					rejectedPeaks.append(temp2)

				if temp3:
					allPeaks = temp3

				if temp4:
					new_annotations.append(temp4)
			if allPeaks:
				for i in allPeaks:
					for p2 in allPeaks:
						if i['peak_id_id'] == p2['peak_id_id']:
							if i['valued'] != p2['valued']:
								incr += 1
			context['notAnnotatedPeaks'] 	= context["totalPeaksForCampaign"]-len(annotatedPeaks)
			context['AnnotatedPeaks'] 		= len(annotatedPeaks)
			#list of peaks who have been annotated at least once.
			context['annotatedList'] 		= Peak.objects.filter(id__in = annotated_peaks).exclude(id__in = new_annotations).values()
			#list of peaks with at least one rejected annotatio
			context['rejectedList']			= Peak.objects.filter(id__in = rejected_peaks).values()
			#peaks who have new annotations
			context['new_annotations']      = Peak.objects.filter(id__in = new_annotations).values()
			#campaign peaks not annotated
			context["campaign_peaks"] 		= Peak.objects.filter(campaign_id = self.kwargs['pk'], status=1).exclude(id__in = annotated_peaks).values()
			#print(rejected_peaks)
			context['RejectedPeaks'] 		= len(rejectedPeaks)
			context['conflix']				= incr
		return context

	def post(self, request, *args, **kwargs):
		if self.request.is_ajax():
			mydata = json.loads(request.body)
			if request.method == 'POST' and mydata['action'] == 'getPeakDataForAdmin':
				#print(mydata['action'])
				peaks1 = list(Peak.objects.filter(id = mydata['peak_id']).values())
				annotation_evaluated  = list(Peak_annotations.objects.filter(peak_id = mydata['peak_id']).values())
				positive = 0
				negative = 0
				if annotation_evaluated:
					for i in annotation_evaluated:
						if i['valued'] == 1:
							positive += 1
						elif i['valued'] == 0:
							negative += 1
				print(negative)
				print(positive)
				data = {
					'peaks_json':peaks1, 
					'annotations':annotation_evaluated,
					'positive':positive,
					'negative':negative
					}
				return JsonResponse({'peaks': data},content_type='application/json')
		else:
			if 'evaluateAnnotationForm' in request.POST:
				#print("okay we in")
				self.object 			= None
				annotation_peak 		= self.request.POST.get('hidden_peak_id')
				annotation 				= Peak_annotations.objects.get(id = annotation_peak)

				annotation.status 		= self.request.POST.get('evaluateAnnotation')
				campaign_id 			= self.request.POST.get('act_cpm')
				#annotation.valued 		= True
				#print(annotation.status)
				#post.campaign_id	= Campaign.objects.get(id = request.POST.get('id'))
				#post.user_id   	= request.user
				annotation.save()
				messages.success(request, 'You revied the annotaion')
				return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': campaign_id}))
			elif 'addPeakForm' in request.POST:
				self.object = self.get_object()
				form = self.get_form()
				if form.is_valid():
					return self.form_valid(form)
				else:
					messages.warning(request,  form.errors)
					return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': self.object.id}))
		return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': self.object.id}))

	def test_func(self):
		if self.request.user.is_manager == True:
			return True
		return False

	def handle_no_permission(self):
		self.object = self.get_object()
		if self.raise_exception:
			raise PermissionDenied(self.get_permission_denied_message())
		return HttpResponseRedirect(reverse('peak-list', kwargs={'pk': self.object.id}))

	def form_valid(self,form):
		form.fields = self.object
		#form.instance.name gets the name of the tag field
		mydata 		= form.instance.fileJson
		mydataTemp	= json.load(mydata)
		mydataTemp 	= json.dumps(mydataTemp)
		mydata3 	= json.loads(mydataTemp)

		#status of the uploaded peak
		status 		= form.instance.status
		peak_exists = []
		i = 0
		for data in mydata3:
			#self.object gets here the Entity we are viweing
			form.instance.id 			= None
			form.instance.peak_id 		= data['id']
			form.instance.lat 			= data['latitude']
			form.instance.lon			= data['longitude']
			form.instance.alt			= data['elevation']
			form.instance.localize_names= data['localized_names']
			form.instance.provenance_org= data['provenance']
			form.instance.name 			= data['name']
			form.instance.campaign_id 	= self.object
			form.instance.status 		= status

			peak_check = Peak.objects.filter(peak_id = data['id'],campaign_id= self.object).values()
			if peak_check:
				#peak_exists = peak_exists + data
				print("exists")
			else:
				print("IN")
				i = i + 1
				form.save()

			print(peak_check)
		if i > 0:
			return super().form_valid(form)
		else:
			messages.error(self.request,"The file you tried to add has all the Peaks already registered ")
			return HttpResponseRedirect(reverse('campaign-detail', kwargs={'pk': self.object.id}))



# creatign a new campaign
class CampaignCreateView(UserPassesTestMixin,LoginRequiredMixin,CreateView):
	model = Campaign
	# passing the field for the form for each campaign
	#fields = ['name','status','start_date','end_date']
	form_class = Create_campaigns
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
	model 		   		= Campaign
	template_name  		= 'campaign/campaign_update.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'campaign-update'
	form_class 			= Update_Campaign
	# passing the field for the form for each campaign
	#fields = ['name','status','start_date','end_date']

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



def CheckUserEnroll(campaign,user):
	hasEnrolled = Campaign_enrollment.objects.filter(campaign_id = campaign,user_id=user)
	if hasEnrolled:
		return hasEnrolled
	return False



register = template.Library()
@register.filter(name='ifUserEnrolled')
def ifUserEnrolled(value, arg):
    return True