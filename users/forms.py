from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.utils.safestring import mark_safe

from .models import User


class ImageWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(
            name,
            value,
            attrs={'class': 'w-100 mt-3', 'id': 'browse'},
            **kwargs,
        )
        img_html = mark_safe(
            f'<img src="{value.url}" class="w-100" id="current-avatar"/>',
        )
        return f'{img_html}{input_html}'


class UserAuthenticationForm(forms.Form):
    email = forms.EmailField(
        validators=[validators.validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = None


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['email', 'username', 'timezone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Confirm password'},
        )


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'avatar']


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Old password'})
        self.fields['new_password1'].widget.attrs.update(
            {'placeholder': 'New password'},
        )
        self.fields['new_password2'].widget.attrs.update(
            {'placeholder': 'Confirm new password'},
        )


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'timezone', 'riot_id', 'riot_tag', 'avatar']

    avatar = forms.ImageField(widget=ImageWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['timezone'].widget.attrs.update({'class': 'w-100'})
        self.fields['riot_tag'].widget.attrs.update(
            {'class': 'form-control', 'id': 'inlineFormInputGroup'},
        )
