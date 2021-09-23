from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import create_document_type, getDocumentTypeObject, EditorView, DocumentCreatedListView, DocumentWorkFlowAddView, DocumentExecutionListView, DocumentVerificationView


app_name = 'workflow'

urlpatterns = [
    path('editor/', login_required(EditorView.as_view()), name='editor'),
    path('created-document-list/', login_required(DocumentCreatedListView.as_view()), name='created-document-list'),
    path('create-document-type/', login_required(create_document_type), name="create-document-type"),
    path('detail-document-type/<int:id>', login_required(getDocumentTypeObject), name="detail-document-type"),
    path('add-document/', login_required(DocumentWorkFlowAddView.as_view()), name="add-document"),
    path('documents-in-workflow/', login_required(DocumentExecutionListView.as_view()), name="documents-in-workflow"),
    path('verify-document/<int:id>', login_required(DocumentVerificationView.as_view()), name="verify-document")
]


