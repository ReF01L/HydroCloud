from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from account.forms import UserRegistrationForm, UserLoginForm
from account.models import Profile
from account.ssh import SSH


def command(request):
    user = Profile.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'content': SSH().command('ls -la'), 'user': user})


@require_GET
def profile(request):
    if not request.user.is_anonymous:
        user = Profile.objects.get(user=request.user)
        return render(request, 'account/profile.html', {'user': user})
    return home(request, False)


def home(request, error):
    if not request.user.is_anonymous:
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
    return redirect('account:user_login')


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
            Profile.objects.create(user=User.objects.get(id=user.id))
            return redirect('account:user_login')
        error = True
    return home(request, error)
