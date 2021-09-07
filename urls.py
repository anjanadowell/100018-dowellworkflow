from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import WorkFlowCreateView, WorkFlowDetailView, DocumentWorkFlowAddView, DocumentExecutionListView, DocumentVerificationView


app_name = 'workflow'

urlpatterns = [
    path('create/', WorkFlowCreateView.as_view(), name="create"),
    path('detail/<int:id>', WorkFlowDetailView.as_view(), name="detail"),
    path('add-document/', DocumentWorkFlowAddView.as_view(), name="add-document"),
    path('documents-in-workflow/', DocumentExecutionListView.as_view(), name="documents-in-workflow"),
    path('verify-document/<int:id>', DocumentVerificationView.as_view(), name="verify-document")
]
