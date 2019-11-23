from django.db import models
from django.db import models
from users import models as user_models
from django.utils import timezone
from datetime import date
from django.urls import reverse

# Create your models here.
class Campaign(models.Model):
	name 		= models.CharField(max_length=200)
	user_id 	= models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE)
	status 		= models.CharField(max_length=10)
	date_posted = models.DateField(default=timezone.now)
	start_date  = models.DateField(default=timezone.now)
	end_date 	= models.DateField()

	def __str__(self):
		return self.name
	#method to find the url to a specific campaign
	def get_absolute_url(self):
		return reverse('campaign-detail', kwargs={'pk': self.pk})

