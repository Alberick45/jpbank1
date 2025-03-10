# jpbankApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CoreUser

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = CoreUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CoreUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user