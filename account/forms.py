from django import forms
from django.contrib.auth.models import User

from account import consts
from account.models import Profile, Algorithm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'input',
        }
    ))
    password = forms.CharField(label='Пароль', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Пароль',
            'class': 'input',
        }
    ))

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.errors.clear()


class EmailCodeForm(forms.ModelForm):
    code = forms.IntegerField(label='Код', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Код',
            'class': 'input',
        }
    ))

    class Meta:
        model = Profile
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not Profile.objects.filter(code=code).exists():
            self.fields['code'].widget.attrs.update({
                'class': 'input-error',
                'placeholder': 'Incorrect code',
            })
            raise forms.ValidationError('')
        return code


class UserRegistrationForm(forms.ModelForm):
    error_css_class = 'error'

    first_name = forms.CharField(label='Имя', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Ваше имя',
            'class': 'input',
        }
    ))
    last_name = forms.CharField(label='Фамилия', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Ваша фамилия',
            'class': 'input',
        }
    ))
    username = forms.CharField(label='Имя пользователя', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Имя пользователя',
            'class': 'input',
        }
    ))
    email = forms.CharField(label='Email', label_suffix='', widget=forms.EmailInput(
        attrs={
            'placeholder': 'Ваш Email',
            'class': 'input',
        }
    ))
    password = forms.CharField(label='Пароль', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Введите пароль',
            'class': 'input',
        }
    ))
    password2 = forms.CharField(label='Повторите пароль', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Повторите пароль',
            'class': 'input',
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                self.fields['email'].widget.attrs.update({
                    'class': 'input-error',
                    'placeholder': 'Email уже занят',
                })
                raise forms.ValidationError('')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            self.fields['username'].widget.attrs.update({
                'class': 'input-error',
                'placeholder': 'Имя пользователя уже занято',
            })
            raise forms.ValidationError('')
        return username


class ChooseAlgForm(forms.Form):
    name = forms.ChoiceField(label='', label_suffix='', choices=consts.Algorithms.choices, widget=forms.Select(
        attrs={
            'class': 'input'
        }
    ))

    class Meta:
        model = Algorithm
        fields = ('name',)


class VolumetricScatterFilteringForm(forms.Form):
    height = forms.IntegerField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Кол-во строк входной матрицы',
            'class': 'input'
        }
    ))
    width = forms.IntegerField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Ширина строки входной матрицы',
            'class': 'input'
        }
    ))
    start = forms.IntegerField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Начальная строка вычисления сигмы',
            'class': 'input'
        }
    ))
    end = forms.IntegerField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Конечная строка вычисления сигмы',
            'class': 'input'
        }
    ))
    data = forms.FileField(label='Load JSF file', label_suffix='')


class MedianFilteringForm(forms.Form):
    param1 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    param2 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param2',
            'class': 'input'
        }
    ))
    data = forms.FileField(label='Load JSF file', label_suffix='')


class DoubleFilteringForm(forms.Form):
    param1 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    data = forms.FileField(label='Load JSF file', label_suffix='')


class LogarithmicFilteringForm(forms.Form):
    param1 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    param2 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    param3 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    param4 = forms.CharField(label='', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'param1',
            'class': 'input'
        }
    ))
    data = forms.FileField(label='Load JSF file', label_suffix='')
