from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import WorkFlowModel, DocumentType, Document
from .forms import DocumentForm

# Create your views here.


class WorkFlowCreateView(CreateView):
	model = WorkFlowModel
	success_message = '%(title)s was created successfully'
	template_name = 'workflow/create.html'
	fields = [
		'title', 'steps'
	]



class WorkFlowDetailView(DetailView):
	model = WorkFlowModel
	template_name = 'workflow/detail.html'

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(WorkFlowModel, id=id_)



class DocumentWorkFlowAddView(View):
	form = DocumentForm()

	def get(self, request):
		return render(request, 'workflow/execute.html', context={'form': self.form})

	def post(self, request):
		doc = Document(document_name=request.POST['document_name'], document_type=request.POST['document_type'], notify_users = True)
		doc.save()
		messages.success(request, doc.document_name + ' - Added In WorkFlow - '+ doc.document_type.title)
		return redirect('workflow:documents-in-workflow')


class DocumentExecutionListView(ListView):
	model = Document
	paginated_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


def execute(user,status, wf):
	authority = wf.steps.all()[status].authority

	if(request.user == authority):

		if :
			status += 1
			messages.success(request, 'Document Signed at :'+ wf.steps.all()[status_value - 1].name)

		else:
			msg = 'Document Signed at all stages.'
	else:
		msg = 'NOT OK, You are NOT authorised'
		

class DocumentVerificationView(View):
	def get(self, request, **kwargs):
		id_ = kwargs.get('id')
		obj = get_object_or_404(Document, id=id_)
		return render(request, 'workflow/document_verify.html', { 'object': obj })

	def post(self, request, **kwargs):
		id_ = kwargs.get('id')
		doc = get_object_or_404(Document, id=id_)

		execute_response = None

		if doc.document_type.internal_work_flow and doc.internal_status < len(doc.document_type.internal_work_flow.steps.all()):
			execute_response = execute(request.user, doc.internal_status, internal_work_flow)

		elif doc.document_type.external_work_flow and doc.external_status < len(doc.document_type.external_work_flow.steps.all()):
			execute_response = execute(request.user, doc.external_status, external_work_flow)

		else:
			execute_response = 'No WorkFlow Available'

		return HttpResponse(execute_response)


