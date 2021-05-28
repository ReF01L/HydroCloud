from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .context_processor import ssh

from HydroCloud import settings
from account.forms import UserRegistrationForm, UserLoginForm


def command(request, command):
    if settings.SSH_SESSION_CLIENT not in request.session:
        request.session[settings.SSH_SESSION_CLIENT] = {}
    request.session[settings.SSH_SESSION_CLIENT]['client'].command(command)
    return redirect('account:profile')


def profile(request):
    if settings.SSH_SESSION_CLIENT not in request.session:
        request.session[settings.SSH_SESSION_CLIENT] = {}
    return render(request, 'account/profile.html', {'content': request.session.get(settings.SSH_SESSION_CLIENT).get('content')})


def home(request, error):
    if 'user' in request.session:
        return profile(request)
    if request.path == '/account/login/':
        return render(request, 'account/login.html', {
            'form': UserLoginForm(),
            'error': error
        })
    elif request.path == '/account/register/':
        return render(request, 'account/register.html', {
            'form': UserRegistrationForm(),
            'error': error
        })


def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@csrf_exempt
def user_login(request):
    error = False
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None and user.is_active:
                if request.POST.get('remember'):
                    request.session['user'] = user
                login(request, user)
                return redirect('account:profile')
        error = True
    return home(request, error)


def register(request):
    error = False
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('account:user_login')
        error = True
    return home(request, error)
