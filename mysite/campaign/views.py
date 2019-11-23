from django.shortcuts import render
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView
	)
from .models import Campaign


# Create your views here.

#this will be the home page for one campaign to check the progress
#peaks etc, this can bee seen only by admin of each campaign


### TO DO :
	# 1) MAKE THIS ACCESIBLE ONLY TO LOGGIN USERS
	# 2) SHOW HERE THE CLICKED POST

def campaign(request):
	return render(request,'campaign/campaign.html')


# class base view
class CampaignListView(ListView):
	model = Campaign
	template_name = 'users/profile.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'campaign'
	ordering = ['-date_posted']

# a view for individual campaign
# here i am sticking to django default template just to show the difference
class CampaignDetailView(DetailView):
	model = Campaign

# creatign a new campaign
class CampaignCreateView(CreateView):
	model = Campaign
	# passing the field for the form for each campaign
	fields = ['name','status','start_date','end_date']

	#checking if form is valid and we add the current user to the form
	def form_valid(self,form):
		#user_id is the id of the user we want to associate to the campaign
		form.instance.user_id = self.request.user
		return super().form_valid(form)

