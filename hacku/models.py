from __future__ import unicode_literals
from django.contrib import admin
from django.db import models

# Create your models here.


class RunUser(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField(primary_key=True)
	score = models.IntegerField(default=-1)
	max_score = models.IntegerField()
	lat = models.DecimalField(default=0, decimal_places=3, max_digits=7)
	long = models.DecimalField(default=0, decimal_places=3, max_digits=7)
	online = models.BooleanField(default=0)
	win = models.IntegerField(default=0)
	opponent_name = models.CharField(max_length=30, default="")
	opponent_score = models.IntegerField(default=-1)
	random_array = models.CharField(max_length=10000)

	def __str__(self):
		return self.name
admin.site.register(RunUser)


class Images(models.Model):
	url = models.URLField()
admin.site.register(Images)

class Online(models.Model):
	email = models.EmailField()
	def __str__(self):
		return self.email
admin.site.register(Online)


class StartTime(models.Model):
	time = models.CharField(max_length=10)
admin.site.register(StartTime)
