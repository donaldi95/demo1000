from django.urls import path
from .views import (
	CampaignDetailView,
	CampaignCreateView
	)
from . import views

urlpatterns = [
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
   #shares a tempalte with the updated view
    path('campaign/new/', CampaignCreateView.as_view(), name='campaign-create'),

]