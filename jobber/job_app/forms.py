from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User as us
from django.contrib.auth.forms import UserCreationForm
from job_app.models import *
from .choices import *


class URF(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = us
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class Createjob(forms.Form):
    title = forms.CharField()
    job_sector = forms.ChoiceField(choices=JOB_SECTOR, initial='1', required=True)
    location = forms.ChoiceField(choices=LOCATION, required=True)
    experience_level = forms.ChoiceField(choices=EXPERIENCE_LEVEL, required=True)
    description = forms.CharField(widget=forms.Textarea)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = us
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = ['phone', 'city', 'website', 'b_date', 'curriculum']