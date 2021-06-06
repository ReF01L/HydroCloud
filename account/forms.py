from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Login', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'login_form-field',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'login_form-field',
            'placeholder': 'Password'
        }
    ))

    class Meta:
        model = User
        fields = ()


class UserRegistrationForm(forms.ModelForm):
    error_css_class = 'error'

    username = forms.CharField(label='Login', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'rg_form-field',
        }
    ))
    email = forms.CharField(label='Email', label_suffix='', widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
            'class': 'rg_form-field',
        }
    ))
    first_name = forms.CharField(label='Name', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'First name',
            'class': 'rg_form-field',
        }
    ))
    last_name = forms.CharField(label='Surname', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Last name',
            'class': 'rg_form-field',
        }
    ))
    password = forms.CharField(label='Password', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'rg_form-field',
        }
    ))
    password2 = forms.CharField(label='Repeat password', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repeat password',
            'class': 'rg_form-field',
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
