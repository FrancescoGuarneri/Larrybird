from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Tweep(User):
	'''Extra field for an user'''
	access_token = models.CharField(max_length = 100)
	access_secret = models.CharField(max_length = 100)