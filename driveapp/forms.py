from django import forms
from .models import users

class postForm(forms.Form): #조회 폼
    search_word = forms.CharField(label='Search Usercar')