from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='อีเมล')

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'ชื่อผู้ใช้งาน',
            'email': 'อีเมล',
        }