from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import DocumentTypeCreateView, DocumentTypeListView, DocumentTypeDetailView, DocumentWorkFlowAddView, DocumentExecutionListView, DocumentVerificationView


app_name = 'workflow'

urlpatterns = [
    path('create-document-type/', DocumentTypeCreateView.as_view(), name="create-document-type"),
    path('list-document-type/', DocumentTypeListView.as_view(), name="list-document-type"),
    path('detail-document-type/<int:id>', DocumentTypeDetailView.as_view(), name="detail-document-type"),
    path('add-document/', DocumentWorkFlowAddView.as_view(), name="add-document"),
    path('documents-in-workflow/', DocumentExecutionListView.as_view(), name="documents-in-workflow"),
    path('verify-document/<int:id>', DocumentVerificationView.as_view(), name="verify-document")
]
