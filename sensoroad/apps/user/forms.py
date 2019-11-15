from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'username'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-appended',
            'placeholder': 'Enter your password',
            'id': 'password',
        }
    ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'username'
        })
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-appended',
            'placeholder': 'Enter password',
            'id': 'password1',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-appended',
            'placeholder': 'Confirm password',
            'id': 'password2',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')