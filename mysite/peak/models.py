from django.db import models
from campaign import models as campaign_model
from django.utils import timezone

# Create your models here.

# for peaks we decided that the status will be or to be annotated or not to be annotated 
# in case the Campaign status is closed also the status of peak will be closed
class Peak(models.Model):
	campaign_id		= models.ForeignKey(campaign_model.Campaign, on_delete=models.CASCADE)
	name 			= models.CharField(max_length=200)