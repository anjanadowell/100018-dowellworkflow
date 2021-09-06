from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import WorkFlowModel, Document
from .forms import DocumentForm

# Create your views here.

class WorkFlowCreateView(CreateView):
	model = WorkFlowModel
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
		doc = Document(doc_name = request.POST['doc_name'],	doc_type = request.POST['doc_type'], work_flow = get_object_or_404(WorkFlowModel ,id=request.POST['work_flow']), notify_users = True)
		doc.save()
		return redirect('workflow:documents-in-workflow')


class DocumentExecutionListView(ListView):
	model = Document
	paginated_by = 10
	

class DocumentVerificationView(View):
	def get(self, request, **kwargs):
		id_ = kwargs.get('id')
		obj = get_object_or_404(Document, id=id_)
		return render(request, 'workflow/document_verify.html', { 'object': obj})

	def put(self, request, **kwargs):
		id_ = kwargs.get('id')
		doc = get_object_or_404(Document, id=id_)

		if(request.user == doc.work_flow.steps.all()[doc.status].authority):
			status_value = doc.status + 1

			if status_value >= len(doc.work_flow.steps.all()):
				return JsonResponse({'Fully Verified': 'OK'})
			else:
				doc.status += 1
				doc.status_name = doc.work_flow.steps.all()[doc.status].name
				doc.save()
				return JsonResponse({'Verified': 'OK'})
		else:
			return JsonResponse({'verified': 'NOT OK, You are NOT authorised'})
