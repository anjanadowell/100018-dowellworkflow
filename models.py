from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=False)
	profile_image 	= models.ImageField(upload_to='static/profile_images', null=True)

	def __str__(self):
		return f'{self.user.username} Profile' 
