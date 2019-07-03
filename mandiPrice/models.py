from django.db import models


# Create your models here.
class MandiPrice(models.Model):
	date=models.CharField(max_length=20)
	district=models.CharField(max_length=100,default="*")
	market=models.CharField(max_length=100,default="*")
	commodity=models.CharField(max_length=100,default="*")
	variety=models.CharField(max_length=100,default="*")
	grade=models.CharField(max_length=100,default="*")
	minP=models.CharField(max_length=100,default="*")
	maxP=models.CharField(max_length=100,default="*")
	modP=models.CharField(max_length=100,default="*")

	def __str__(self):
		return self.district
