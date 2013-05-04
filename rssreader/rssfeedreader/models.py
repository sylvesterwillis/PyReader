from django.db import models

# Create your models here.

class users(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

class feeds(models.Model):
	url = models.CharField(max_length=255)
	userid = models.ManyToManyField(users)
