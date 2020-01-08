from django.urls import path
from campaign.views import CampaignListView
from . import views
from . import views as users_views
urlpatterns = [
	path('',users_views.index,name='index'),
#    path('', CampaignListView.as_view(), name='blog-home'),
]