from django.db import models
from campaign import models as campaign_models
from users import models as user_models
from peak import models as peak_models
# Create your models here.


class Campaign_enrollment(models.Model):
	user_id 			=  	models.ForeignKey(user_models.MyUser,	   on_delete=models.CASCADE)
	campaign_id 		=  	models.ForeignKey(campaign_models.Campaign, on_delete=models.CASCADE)

class Peak_annotations(models.Model):
	isTrue = True
	isFalse = False

	STATUS_CHOICES= [
		(isTrue, True),
		(isFalse, False)
	]
	user_id 			=  	models.ForeignKey(user_models.MyUser, on_delete=models.CASCADE)
	peak_id 	 		= 	models.ForeignKey(peak_models.Peak,    on_delete=models.CASCADE)
	w_name 				= 	models.CharField(max_length=1000,blank=True,null=True)
	#w_localize_names 	= 	models.CharField(blank=True,max_length=300,null=True)
	#w_provenance_org	= 	models.CharField(blank=True,max_length=1000,null=True)
	#w_alt				= 	models.DecimalField(default=0.0,max_digits=22, decimal_places=16)
	status				=	models.BooleanField(default=False)
	valued				=	models.BooleanField(blank=True,null=True,choices=STATUS_CHOICES,)
