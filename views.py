from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import WorkFlowModel, DocumentType, Document
from .forms import DocumentForm

# Create your views here.


class DocumentTypeCreateView(CreateView):
	model = DocumentType
	success_message = '%(title)s was created successfully'
	template_name = 'workflow/create.html'
	fields = [
		'title', 'internal_work_flow', 'external_work_flow'
	]


class DocumentTypeDetailView(DetailView):
	model = DocumentType
	template_name = 'workflow/detail.html'

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(DocumentType, id=id_)



class DocumentWorkFlowAddView(View):
	form = DocumentForm()

	def get(self, request):
		return render(request, 'workflow/execute.html', context={'form': self.form})

	def post(self, request):
		doc = Document(document_name=request.POST['document_name'], document_type=get_object_or_404(DocumentType, id=request.POST['document_type']), notify_users = True)
		doc.save()
		messages.success(request, doc.document_name + ' - Added In WorkFlow - '+ doc.document_type.title)
		return redirect('workflow:documents-in-workflow')


class DocumentExecutionListView(ListView):
	model = Document
	paginated_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


def execute_wf(request, status, wf):
	authority = wf.steps.all()[status].authority

	if request.user == authority :
		status += 1
		if status == len(wf.steps.all()) :
			messages.error(request, 'Document Signed at all stages.')
			
		else:
			messages.success(request, 'Document Signed at :'+ wf.steps.all()[status - 1].name + '.')
	else:
		messages.error(request, 'You are NOT authorised')
		
	return status 



class DocumentVerificationView(View):
	def get(self, request, **kwargs):
		id_ = kwargs.get('id')
		obj = get_object_or_404(Document, id=id_)
		return render(request, 'workflow/document_verify.html', { 'object': obj })

	def post(self, request, **kwargs):
		msg = None
		status = None

		doc = get_object_or_404(Document, id=request.POST['id_'])

		if doc.document_type.internal_work_flow and doc.internal_status < len(doc.document_type.internal_work_flow.steps.all()):
			status = execute_wf(request, doc.internal_status, doc.document_type.internal_work_flow)
			if status and status != doc.internal_status :
				doc.internal_status = status

		elif doc.document_type.external_work_flow and doc.external_status < len(doc.document_type.external_work_flow.steps.all()):
			status = execute_wf(request, doc.external_status, doc.document_type.external_work_flow)
			if status and status != doc.external_status :
				doc.external_status = status

		else:
			messages.error(request, 'No WorkFlow Available')

		doc.save()
		return redirect('workflow:documents-in-workflow')


