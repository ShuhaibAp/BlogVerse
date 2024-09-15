from django import forms
from accounts.models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image','username','bio']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['profile','likes','bookmarks']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=["comment"]
        widgets={
        'comment':forms.Textarea(attrs={"cols":30,"rows":5,"class":"form-control border border-primary"})
        }