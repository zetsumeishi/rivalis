from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from .forms import EditProfileForm
from .forms import UserAuthenticationForm
from .forms import UserCreationForm
from .models import User


@login_required
def edit_profile(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user.
    """
    context = dict()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Profile updated successfully',
            )
            return render(request, 'users/profile.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')

    form_data = {
        'email': request.user.email,
        'username': request.user.username,
        'avatar': request.user.avatar,
        'timezone': request.user.timezone,
        'riot_id': request.user.riot_id,
        'riot_tag': request.user.riot_tag,
    }
    context = {
        'form': EditProfileForm(initial=form_data),
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def profile(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user.
    """
    context = {
        'teams': request.user.team_set.all(),
    }

    return render(request, 'users/profile.html', context)


def log_in(request):
    """User registration view

    This view is used for handling GET and POST request to display the sign up form and
    create the user. Once the account is created, the user is logged in and redirected
    to the home.
    """
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            credentials = {
                'email': email,
                'password': password,
            }
            user = authenticate(request, **credentials)
            if user:
                login(request, user)
                context = {'user': user}
            return HttpResponseRedirect('/')
    else:
        form = UserAuthenticationForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def sign_up(request):
    """User registration view

    This view is used for handling GET and POST request to display the sign up form and
    create the user. Once the account is created, the user is logged in and redirected
    to the home.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            data = {
                'timezone': form.cleaned_data['timezone'] or 'UTC',
                'username': form.cleaned_data['username'],
            }
            user = User.objects.create_user(email=email, password=password, **data)
            login(request, user)
            context = {'user': user}
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'users/sign_up.html', context)


@login_required
def delete_account(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user. Once we deleted the account, the user is redirected to the home.
    """
    request.user.delete()
    return HttpResponseRedirect('/')
