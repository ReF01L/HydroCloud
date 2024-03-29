import datetime
import os
import random
from string import ascii_letters

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
from account.forms import UserRegistrationForm, LoginForm, EmailCodeForm
from account.models import Profile, Algorithm
from . import consts
from .tasks import start_algorithm

algorithm_forms = {
    consts.VOLUMETRIC_SCATTER_FILTERING: VolumetricScatterFilteringForm,
    consts.MEDIAN_FILTERING: MedianFilteringForm,
    consts.DOUBLE_FILTERING: DoubleFilteringForm,
    consts.LOGARITHMIC_FILTERING: LogarithmicFilteringForm
}


def get_params(alg_name, params):
    if alg_name == consts.VOLUMETRIC_SCATTER_FILTERING:
        return consts.get_volumetric_scatter_filtering_dict(params)
    elif alg_name == consts.MEDIAN_FILTERING:
        return consts.get_median_filtering_dict(params)
    elif alg_name == consts.DOUBLE_FILTERING:
        return consts.get_double_filtering_dict(params)
    elif alg_name == consts.LOGARITHMIC_FILTERING:
        return consts.get_logarithmic_filtering_dict(params)
    return None


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
    _profile = Profile.objects.get(user=user)
    algorithms = Algorithm.objects.filter(user=_profile)
    [setattr(algorithm, 'parameters', get_params(algorithm.name, algorithm.params.split(' | '))) for algorithm in algorithms]
    return render(request, 'account/profile.html', {
        'profile': _profile,
        'algorithms': algorithms
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
            _code = generate_code()
            Profile.objects.create(user=user, code=_code)

            theme = 'Activate account HydroCloud'
            email = EmailMessage(theme, f'CODE: {_code}', settings.EMAIL_HOST_USER, [form.cleaned_data['email']])
            email.send()

            return redirect('account:code')

    return render(request, 'account/register.html', {
        'form': form
    })


def code(request):
    if request.method == 'POST':
        form = EmailCodeForm(request.POST)
        if form.is_valid():
            _profile = Profile.objects.get(code=form.cleaned_data['code'])
            user = User.objects.get(email=_profile.user.email)
            user.is_active = True
            user.save()
            _profile.code = '0000'
            _profile.save()
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
                file_name = f'{request.user.username}_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_data.jsf'
                img_name = f'{request.user.username}_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_img.png'
                local_path = os.path.join(settings.BASE_DIR, 'media', 'jsf', file_name)
                # Save file
                with open(local_path, 'wb+') as destination:
                    for chunk in request.FILES['data']:
                        destination.write(chunk)

                params = ' | '.join([str(value) for key, value in cd.items() if isinstance(value, int)])

                jsf_path = local_path
                jsf_output_path = os.path.join(os.path.split(local_path)[0], f'{file_name[:-4]}.txt')
                data_path = os.path.join(settings.BASE_DIR, 'data.txt')
                img_path = os.path.join(settings.BASE_DIR, 'media', 'algs', img_name)

                slug = ''.join(random.choice(ascii_letters) for _ in range(10))
                start_algorithm.delay(jsf_path, jsf_output_path, data_path, img_path, params, slug, request.session['ALG'])
                # Save to db
                Algorithm.objects.create(
                    user=Profile.objects.get(user=request.user),
                    name=request.session['ALG'],
                    params=params,
                    slug=slug,
                    file=request.FILES['data'],
                    status=consts.Statuses.InProcess
                )

                return redirect('account:profile')
    else:
        return render(request, 'account/create_image.html', {
            'choose_alg': ChooseAlgForm(),
        })


def get_all_results(request):
    algorithms = Algorithm.objects.all()
    [setattr(algorithm, 'parameters', get_params(algorithm.name, algorithm.params.split(' | '))) for algorithm in algorithms]
    return render(request, 'account/results_algorithm.html', {
        'algorithms': algorithms
    })
