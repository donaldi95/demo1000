from django.db import models
from users import models as user_models
from django.utils import timezone
from datetime import date
from django.urls import reverse
from .validators import validate_start_date
from django.core.exceptions import ValidationError
# Create your models here.
class Campaign(models.Model):
	Start = 'Start'
	Created = 'Created'
	Closed = 'Closed'

	STATUS_CHOICES= [
		(Start, 'Start'),
		(Created, 'Created'),
		(Closed,'Closed')
	]
	name 		= models.CharField(max_length=200)
	user_id 	= models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE)
	status 		= models.CharField(max_length=10,choices=STATUS_CHOICES,default=Created,)
	date_posted = models.DateField(default=timezone.now)
	start_date  = models.DateField(default=timezone.now)
	end_date 	= models.DateField()

	def __str__(self):
		return self.name
	#method to find the url to a specific campaign
	def get_absolute_url(self):
		return reverse('campaign-detail', kwargs={'pk': self.pk})


	def clean(self):
		# Don't allow draft entries to have a pub_date.
		if self.start_date >= self.end_date:
			raise ValidationError('End Date should be greater than Start date ')

class Enroll(models.Model):
	user_id 	= models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE)
	campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
	def get_absolute_url(self):
		return reverse('campaign-detail', kwargs={'pk': self.pk})
