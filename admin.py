from django.contrib import admin
from .models import WorkFlowModel, VerificationStep

# Register your models here.
admin.site.register(WorkFlowModel)
admin.site.register(VerificationStep)  
