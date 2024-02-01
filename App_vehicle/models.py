from django.db import models
from datetime import date
# Create your models here.
class signup(models.Model):
	name=models.TextField(max_length=30)
	email=models.TextField(max_length=40)
	password=models.TextField(max_length=30)

class vehicles(models.Model):
	uid=models.IntegerField()
	vno=models.TextField(max_length=30)
	yop=models.IntegerField()
	engine_oil=models.TextField()
	repaird=models.IntegerField()
	brake=models.TextField()
	tyre=models.TextField()
	physical=models.TextField(default="NAN")