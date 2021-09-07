from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class VerificationStep(models.Model):
	name 		= models.TextField(max_length=100)
	authority	= models.ForeignKey(User, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return self.name


class WorkFlowModel(models.Model):
	title       	= models.CharField(max_length=100)
	steps			= models.ManyToManyField(VerificationStep, blank=True)
	
	class Meta:
		ordering = ['title']

	def get_absolute_url(self):
		return reverse("workflow:detail", kwargs={"id": self.id})

	def __str__(self):
		return f'{self.title}'


class Document(models.Model):
	doc_name 		= models.CharField(max_length=100, null=False)
	doc_type 		= models.CharField(max_length=100, null=False)
	work_flow 		= models.ForeignKey(WorkFlowModel, on_delete=models.CASCADE, null=True, default=None)
	status 			= models.IntegerField(default=0)
	status_name		= models.CharField(max_length=100, null=True)
	update_time		= models.DateField(null=True)
	notify_users 	= models.BooleanField(default=True)

	def __str__(self):
		return self.doc_name



@receiver(pre_save, sender=Document)
def document_pre_save(sender, instance, *args, **kwargs):
	instance.update_time = timezone.now()
	if instance.status == 0:
		instance.status = 1
		instance.status_name = instance.work_flow.steps.all()[instance.status].name


@receiver(post_save, sender=Document)
def document_post_save(sender, instance, created, *args, **kwargs):
	print('------------------Notifying Users', instance.work_flow.steps.all()[instance.status].authority )
		
