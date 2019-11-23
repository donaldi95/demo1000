from django.urls import path
from .views import (
	CampaignListView,
	CampaignDetailView,
	CampaignCreateView,
	CampaignUpdateView
	)
from . import views

urlpatterns = [
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
   #shares a tempalte with the updated view
    path('campaign/new/', CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:pk>/update/', CampaignUpdateView.as_view(), name='campaign-update'),
	path('campaign', CampaignListView.as_view(), name='campaign-home'),
	
]