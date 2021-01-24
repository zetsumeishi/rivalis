from django.shortcuts import redirect
from django.urls import reverse

from .models import Organization


def is_organization_owner(func):
    def wrapper(request, *args, **kwargs):
        is_owner = Organization.objects.filter(owner=request.user).exists()
        if is_owner:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('organizations:create_organization'))

    return wrapper
