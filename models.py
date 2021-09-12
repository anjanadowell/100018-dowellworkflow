from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class SigningStep(models.Model):
	name 		= models.CharField(max_length=100)
	authority	= models.ForeignKey(User, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return f'{self.name} - {self.authority}'


class WorkFlowModel(models.Model):
	title       = models.CharField(max_length=100)
	steps		= models.ManyToManyField(SigningStep, blank=True)
	
	class Meta:
		ordering = ['title']

	def __str__(self):
		return f'{self.title}'


class DocumentType(models.Model):
	title       			= models.CharField(max_length=100)
	internal_work_flow 		= models.ForeignKey(WorkFlowModel, related_name='%(class)s_internal_wf', on_delete=models.SET_NULL, null=True, blank=True)
	external_work_flow 		= models.ForeignKey(WorkFlowModel, related_name='%(class)s_external_wf', on_delete=models.SET_NULL, null=True, blank=True)


	def get_absolute_url(self):
		return reverse("workflow:detail", kwargs={"id": self.id})

	def __str__(self):
		return self.title

class Document(models.Model):
	document_name 		= models.CharField(max_length=100, null=False)
	document_type 		= models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True)
	internal_status		= models.IntegerField(default=0)
	internal_wf_step	= models.CharField(max_length=100, null=True, blank=True)
	external_status		= models.IntegerField(default=0)
	external_wf_step	= models.CharField(max_length=100, null=True, blank=True)
	update_time			= models.DateField(null=True)
	notify_users 		= models.BooleanField(default=True)

	def __str__(self):
		return self.document_name



@receiver(pre_save, sender=Document)
def document_pre_save(sender, instance, *args, **kwargs):
	instance.update_time = timezone.now()
	
	if instance.document_type.internal_work_flow and instance.document_type.external_work_flow :
		instance.internal_wf_step = instance.document_type.internal_work_flow.steps.all()[instance.internal_status].name
		instance.external_wf_step = instance.document_type.external_work_flow.steps.all()[instance.external_status].name
	elif instance.document_type.internal_work_flow :
		instance.internal_wf_step = instance.document_type.internal_work_flow.steps.all()[instance.internal_status].name
	elif instance.document_type.external_work_flow :
		instance.external_wf_step = instance.document_type.external_work_flow.steps.all()[instance.external_status].name
	else:
		pass

@receiver(post_save, sender=Document)
def document_post_save(sender, instance, created, *args, **kwargs):
	print('------------------Notifying Users')
		

