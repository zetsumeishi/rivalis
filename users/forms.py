from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import ImageField
from django.forms import ModelForm
from django.forms import widgets
from django.utils.safestring import mark_safe

from .models import User


class AvatarWidget(widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img src="{value.url}"/>')
        return f'{input_html}{img_html}'


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['email', 'username', 'timezone']


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'avatar']


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'avatar', 'timezone']
        exclude = ['password']

    avatar = ImageField(widget=AvatarWidget)
