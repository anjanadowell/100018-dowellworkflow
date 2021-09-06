from django.contrib import admin
from .models import WorkFlowModel, VerificationStep, Document

# Register your models here.
admin.site.register(WorkFlowModel)
admin.site.register(VerificationStep)
admin.site.register(Document)  
