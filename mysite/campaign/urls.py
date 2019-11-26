from django.urls import path
from .views import (
	CampaignListView,
	CampaignDetailView,
	CampaignCreateView,
	CampaignUpdateView,
	CampaignDeleteView,
	#PeakCreateView,
	)
from . import views

urlpatterns = [
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
  	#path('campaign/<int:pk>/newpeak/', PeakCreateView.as_view(), name='peak-create'),
   #shares a tempalte with the updated view
    path('campaign/new/', CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:pk>/update/', CampaignUpdateView.as_view(), name='campaign-update'),
	path('campaign/<int:pk>/delete/', CampaignDeleteView.as_view(), name='campaign-delete'),
	path('campaign/', CampaignListView.as_view(), name='campaign-home'),
	
]