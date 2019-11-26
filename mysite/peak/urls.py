from django.urls import path
from . import views


from .views import (
	PeakListView,
	)


urlpatterns = [

    path('campaign/<int:pk>/peak/', PeakListView.as_view(), name='peak-list'),

    ]