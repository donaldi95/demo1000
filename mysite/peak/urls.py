from django.urls import path
from . import views


from .views import (
	PeakListView,
	PeakDetailView,
	)


urlpatterns = [
    path('campaign/<int:campaign_id>/peak/<int:pk>', PeakDetailView.as_view(), name='peak-detail'),
    path('campaign/<int:pk>/peak/', PeakListView.as_view(), name='peak-list'),

    ]