from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class EgLoginForm(forms.Form):
    username=forms.CharField(max_length=20,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))

class ERegForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']
        widgets={
        'first_name':forms.TextInput(attrs={"class":"form-control","placeholder":"First Name"}),
        'last_name':forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name"}),
        'email':forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}),
        'username':forms.TextInput(attrs={"class":"form-control ","placeholder":"Username"}),
        }
    password1 = forms.CharField(
            label=("Password"),
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control","placeholder":"Password"}),
            help_text=password_validation.password_validators_help_text_html(),
        )
    password2 = forms.CharField(
            label=("Password confirmation"),
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control ","placeholder":"Confirm Password"}),
            strip=False,
            help_text=("Enter the same password as before, for verification."),
        )