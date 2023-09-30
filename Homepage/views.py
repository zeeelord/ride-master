from django.shortcuts import render
import requests
from .models import *
from django.views.generic import View
from django.contrib import messages
import schedule
import time
from Delevery.models import BaseModel
# Create your views here.


def home(request):

    user = request.user
    jobs = BaseModel.objects.all().order_by('-date')[:5]

    context = {'user': user, 'jobs': jobs}

    return render(request, 'Home/homepage.html', context)

