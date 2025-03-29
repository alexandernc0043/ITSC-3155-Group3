from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]

class PasswordChange(PasswordChangeForm):
    option = forms.ChoiceField(choices=[('no', 'No'), ('yes', 'Yes')])
    class Meta:
        model = User
        fields = ["option", "old_password", "new_password1", "new_password2"]
    