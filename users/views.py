from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from .forms import ProfileForm
from .forms import UserCreationForm
from .models import User


@login_required
def profile(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user.
    """
    context = dict()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Profile updated successfully',
            )
        else:
            messages.add_message(request, messages.ERROR, 'Mistakes were made')
    form_data = {
        'email': request.user.email,
        'username': request.user.username,
        'avatar': request.user.avatar,
        'timezone': request.user.timezone,
    }
    context['form'] = ProfileForm(initial=form_data)
    return render(request, 'users/profile.html', context)


def signup(request):
    """User registration view

    This view is used for handling GET and POST request to display the sign up form and
    create the user. Once the account is created, the user is logged in and redirected
    to the home.
    """
    context = dict()
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
            context['user'] = user
            return HttpResponseRedirect('/')
    context['form'] = UserCreationForm()
    return render(request, 'users/signup.html', context)


@login_required
def delete_account(request):
    """User profile view

    This view is used for handling GET and POST request to display and update the
    user. Once we deleted the account, the user is redirected to the home.
    """
    request.user.delete()
    return HttpResponseRedirect('/')
