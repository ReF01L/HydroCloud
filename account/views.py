import datetime
import os
import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from HydroCloud import settings
from account.forms import UserRegistrationForm, LoginForm, EmailCodeForm, ChooseAlgForm, VolumetricScatterFilteringForm, \
    MedianFilteringForm, DoubleFilteringForm, LogarithmicFilteringForm
from account.models import Profile
from account.forms import UserRegistrationForm, LoginForm, EmailCodeForm
from account.models import Profile, Algorithm
from account.ssh import SFTP, SSH
from . import algorithms

algorithm_forms = {
    'Volumetric Scatter Filtering': VolumetricScatterFilteringForm,
    'Median Filtering': MedianFilteringForm,
    'Double Filtering': DoubleFilteringForm,
    'Logarithmic Filtering': LogarithmicFilteringForm
}


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


@login_required(login_url='/account/login/')
def profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user)
    algorithms = Algorithm.objects.filter(user=profile)
    [setattr(algorithm, 'parameters', algorithm.params.split(' | ')) for algorithm in algorithms]
    # sftp = SFTP()
    # # GET
    # local_path = 'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\account\\paralleled.cpp'
    # remote_path = '/home/dsalushkin/mpi/paralleled.cpp'
    # sftp.get_file(local_path, remote_path)
    # # PUT
    # local_path = 'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\account\\views.py'
    # remote_path = '/home/dsalushkin/mpi/views.py'
    # sftp.put_file(local_path, remote_path)
    return render(request, 'account/profile.html', {'profile': profile,
                                                    'algorithms': algorithms})


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


@login_required(login_url='/account/login/')
def create_image(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name is not None:
            request.session['ALG'] = name
            request.session.save()
            return render(request, 'account/create_image.html', {
                'choose_alg': ChooseAlgForm(request.POST),
                'form': algorithm_forms[name]()
            })
        else:
            form = algorithm_forms[request.session['ALG']](request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                file_name = f'{request.user.username}_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_data.txt'
                local_path = os.path.join(f'{settings.BASE_DIR}\\media\\{file_name}')
                # Save file
                with open(local_path, 'wb+') as destination:
                    for chunk in request.FILES['data']:
                        destination.write(chunk)
                # Send file to cluster
                params = ' | '.join([f'{key} - {value}' for key, value in cd.items() if isinstance(value, str)])
                sftp = SFTP()
                remote_path = f'/home/dsalushkin/mpi/{file_name}'
                sftp.put_file(local_path, remote_path)
                return redirect('account:profile')
    else:
        return render(request, 'account/create_image.html', {
            'choose_alg': ChooseAlgForm(),
        })


def get_file(request):
    # sftp = SFTP()
    # local_path = 'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\account\\test.py'
    # remote_path = '/home/dsalushkin/mpi/test.py'
    # sftp.put_file(local_path, remote_path)
    # return HttpResponse(SSH().command('python3 /home/dsalushkin/mpi/parser.py data.jsf'))
    return HttpResponse("GET FILE")


def get_all_results(request):
    algorithms = Algorithm.objects.all()
    [setattr(algorithm, 'parameters', algorithm.params.split(' | ')) for algorithm in algorithms]
    return render(request, 'account/results_algorithm.html', {'algorithms': algorithms})
