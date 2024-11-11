from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class PharmacistRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class PharmacistLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class DoctorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class DoctorLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']