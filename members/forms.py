from tkinter import Widget
from django.contrib.auth.forms import UserCreationForm
from booking.models import Persona, Doctor, SERVICE_CHOICES, GENDER_CHOICES, ACCOUNT_CHOICES
from django import forms
from django.db import models

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control form-control-lg', 'placeholder': 'example@gmail.com'}))
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    birth_date = forms.DateField(required=True, help_text="*Enter using the YYYY-MM-DD format. Include hyphens.")
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = Persona
        fields = ('email', 'name', 'birth_date', 'gender', 'phone_no', 'kin_name', "kin_contact")

    def __init__(self, *args, **kwargs):
            super(RegisterUserForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'

class RegisterDoctorForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control form-control-lg', 'placeholder': 'example@gmail.com'}))
    name = forms.CharField(label='Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    birth_date = forms.DateField(required=True, help_text="*Enter using the YYYY-MM-DD format. Include hyphens.")
    role = forms.ChoiceField(choices=SERVICE_CHOICES)
    image = forms.FileField(widget=forms.FileInput({'class':'form-control form-control-lg'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = Doctor
        fields = ('email', 'name', 'birth_date', 'account_type', 'gender', 'phone_no', 'role', 'image')

    def __init__(self, *args, **kwargs):
            super(RegisterDoctorForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['image'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['image'].required = False
            self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
            self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'