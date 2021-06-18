import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from HydroCloud import settings
from account.forms import UserRegistrationForm, LoginForm, EmailCodeForm
from account.models import Profile


def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@csrf_exempt
def user_login(request):
    form = LoginForm(request.POST or None)
    error = False
    if request.method == 'POST':
        error = True
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('account:profile')
    return render(request, 'account/login.html', {
        'form': form,
        'error': error
    })


def register(request):
    def generate_code() -> str:
        random.seed()
        return str(random.randint(1000, 9999))

    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                user = User.objects.get(email=form.cleaned_data['email'])
                user.delete()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            code = generate_code()
            Profile.objects.create(user=user, code=code)

            theme = 'Activate account HydroCloud'
            email = EmailMessage(theme, f'CODE: {code}', settings.EMAIL_HOST_USER, [form.cleaned_data['email']])
            email.send()

            return redirect('account:code')

    return render(request, 'account/register.html', {
        'form': form
    })


def code(request):
    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(code=form.cleaned_data['code'])
            user = User.objects.get(email=profile.user.email)
            user.is_active = True
            user.save()
            profile.code = '0000'
            profile.save()
            return redirect('account:user_login')
    return render(request, 'account/register_code.html', {
        'form': EmailCodeForm()
    })
