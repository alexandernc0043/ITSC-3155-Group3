from django.forms import ModelForm

from .models import User

# use setpasswordform
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']