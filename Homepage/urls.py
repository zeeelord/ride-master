from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


app_name = 'Homepage'


urlpatterns = [

    path('', views.home, name='home'),

]
