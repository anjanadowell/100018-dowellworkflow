from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from products.models import Product
from .models import WorkFlowModel
from .utils import document_signing_process

# Create your views here.

class WorkFlowCreateView(CreateView):
	model = WorkFlowModel
	template_name = 'create.html'
	fields = [
		'title', 'steps'
	]


class WorkFlowDetailView(DetailView):
	model = WorkFlowModel
	template_name = 'detail.html'

	def get_object(self):
		id_ = self.kwargs.get('id')
		return get_object_or_404(WorkFlowModel, id=id_)

class WorkFlowExecuteView(View):
	def post(self, request):
		print(request.POST)
		product_object = get_object_or_404(Product, id=request.POST['object_id'])
		work_flow = get_object_or_404(WorkFlowModel, title=request.POST['wf_name'])

		product_object = document_signing_process(product_object, work_flow)
		return redirect('home')

