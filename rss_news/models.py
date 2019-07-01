from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10000)
    published_date=models.CharField(max_length=100,default="",blank=True,null=True)
    source=models.CharField(max_length=100,default="",blank=True,null=True)
    link=models.CharField(max_length=100,default="",blank=True,null=True)
    summary=models.CharField(max_length=10000,default="",blank=True,null=True)
    content=models.CharField(max_length=1000000,default="",blank=True,null=True)


    def __str__(self):
    	return self.title