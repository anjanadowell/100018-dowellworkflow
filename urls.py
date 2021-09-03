from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import UserRegistrationView, UserLoginView, UserProfileUpdateView, logout_view




urlpatterns = [    
    path('logout/', logout_view, name="logout"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update/<int:id>/', login_required(UserProfileUpdateView.as_view()), name='profile-update'),
    path('register/', UserRegistrationView.as_view(), name='register')
]
