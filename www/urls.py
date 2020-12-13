from django.urls import path

from . import views

app_name = 'www'

urlpatterns = [
    path('', views.home, name='home'),
]
