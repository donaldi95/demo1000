from django.db import models
from campaign import models as campaign_model
from django.utils import timezone

# Create your models here.


# for peaks we decided that the status will be or to be annotated or not to be annotated 
# in case the Campaign status is closed also the status of peak will be closed
class Peak(models.Model):
	peak_id			= models.IntegerField(blank=True)
	campaign_id		= models.ForeignKey(campaign_model.Campaign, on_delete=models.CASCADE)
	name 			= models.CharField(max_length=1000,blank=True,null=True)
	localize_names  = models.CharField(blank=True,max_length=300,null=True)
	provenance_org	= models.CharField(blank=True,max_length=1000,null=True)
	lat 			= models.DecimalField(default=0.0,max_digits=22, decimal_places=16)
	lon 			= models.DecimalField(default=0.0,max_digits=22, decimal_places=16)
	alt				= models.DecimalField(default=0.0,max_digits=22, decimal_places=16)
	status		 	= models.BooleanField(default=True)
	date_posted 	= models.DateField(default=timezone.now)
	fileJson 		= models.FileField(upload_to='profile_pics')