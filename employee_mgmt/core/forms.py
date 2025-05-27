from django import forms
from .models import Employee, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']
