from django.urls import path
from campaign.views import CampaignListView
from . import views

urlpatterns = [
    path('', CampaignListView.as_view(), name='blog-home'),
]