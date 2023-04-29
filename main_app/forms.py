from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class AddItemForm(forms.Form):
    url = forms.URLField(label = "Enter the URL")
    desired_price = forms.FloatField(label = "Enter desired price")
    
    
class UserRegistartionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
