from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileForm
from .models import Profile


@login_required
def logout_view(request):
	logout(request)
	return redirect('home')


class UserRegistrationView(View):
	form_1 = UserRegistrationForm()
	form_2 = ProfileForm()

	value_name = 'Register'
	def get(self, request):
		context = {
				'form_1': self.form_1,
				'form_2': self.form_2,
				'value_name': self.value_name
			}
		return render(request, 'users/registration_form.html', context)

	def post(self, request):
		form_1 = UserRegistrationForm(request.POST)
		form_2 = ProfileForm(request.POST, request.FILES)
		if form_1.is_valid() and form_2.is_valid():
			form_1.save()
			form_2.save()
			return redirect('login')
		return render(request, 'users/registration_form.html', {'form_1': self.form_1, 'form_2': self.form_2, 'value_name': self.value_name})


class UserLoginView(UserRegistrationView):
	form_1 = UserLoginForm()
	form_2 = None
	value_name = "Log In"
	def post(self, request):
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect('/', {'user': user})
		else:
			print('Could not Logged In', request.POST['username'])
			return redirect('login')


class UserProfileUpdateView(UpdateView):
	form_1 = UserUpdateForm()
	form_2 = ProfileForm()
	template_name = 'users/registration_form.html'
	value_name = 'Update'
	user = None
	
	def get(self, request, id, **kwargs):
		if request.user.id == id :
			context = {
					'value_name' : self.value_name,
					'form_1' : self.form_1,
					'form_2' : self.form_2,
				}
			return render(request, self.template_name, context)
		else:
			return redirect('login') 

	def post(self, request, id, **kwargs):
		form_1 = UserUpdateForm(request.POST, instance=get_object_or_404(User, id=id))
		form_2 = ProfileForm(request.POST, request.FILES, instance=get_object_or_404(Profile, user=id))
		if request.user.id == id :
			if form_1.is_valid() and form_2.is_valid():
				form_1.save()
				form_2.save()
				return redirect('home')

			else:
				context = {
					'value_name' : self.value_name,
					'form_1' : self.form_1,
					'form_2' : self.form_2,
					'message': 'form not valid'
				}
				return render(request, self.template_name, context)
		
		return redirect('login') 
		


# def get_object(self):
# 	id_ = self.kwargs.get('id')
# 	return get_object_or_404(User, id=id_)

# def get_context_data(self, **kwargs):
# 	context = super().get_context_data(**kwargs)
# 	context['value_name'] = self.value_name
# 	print(context['form'])
# 	return context






# Create your views here.
def home_view(request):
	return render(request, 'home.html', {})

def about_view(request):
	return render(request, 'about.html', {})

def contact_view(request):
	return render(request, 'contact.html', {})
