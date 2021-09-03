from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkFlowCreateView, WorkFlowDetailView, WorkFlowExecuteView


app_name = 'workflow'

urlpatterns = [    
    path('create/', WorkFlowCreateView.as_view(), name="work-flow-create"),
    path('work-flow-detail/<int:id>', WorkFlowDetailView.as_view(), name="work-flow-detail"),
    path('work-flow-execute/', WorkFlowExecuteView.as_view(), name="work-flow-execute")

]
