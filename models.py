from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class VerificationStep(models.Model):
	name 		= models.TextField(max_length=100)
	authority	= models.ForeignKey(User, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return self.name

class WorkFlowModel(models.Model):
	title       	= models.CharField(max_length=100)
	steps			= models.ManyToManyField(VerificationStep)
	
	class Meta:
		ordering = ['title']

	def get_absolute_url(self):
		return reverse("workflow:work-flow-detail", kwargs={"id": self.id})

	def __str__(self):
		return f'{self.title}'

