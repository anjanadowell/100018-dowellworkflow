from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile

class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
		]

class UserLoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = [
			'username','password'
		]

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username', 'first_name', 'last_name', 'email'
		]

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'profile_image'
		]

