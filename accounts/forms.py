from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationForm(AuthenticationForm):
    
    pass


class UserForm(UserCreationForm):
    
    pass