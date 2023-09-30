from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic
from .forms import *
from .models import CustomUserManager, UserModel
from django.views.generic import View
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.db.models import Max, Sum, Avg

# from django import forms
from django.contrib.auth import get_user_model
# from Transactions.models import Withdrawal


class UserCreateView(View):
    form_class = UserCreationForm
    template_name = 'User/signup.html'

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # new = form.save(commit=False)
            # new.phone = '+' + new.phone
            # new.save()

            messages.success(request, "Staff has been created successfully")

            return redirect('userprofile:login')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('homepage'))
        return render(request, 'User/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            # print('Yes')
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Homepage:home'))
            else:
                return render(request, 'User/login.html',
                              {'error_message': 'Your account has been disabled'})
        else:
            # messages.error(request, "Invalid login details")
            return render(request, 'User/login.html')


class LogoutView(View):
    form_class = UserForm
    template_name = '#'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('Homepage:home'))


def get_user(request):

    if request.user != request.user:
        raise Http404

    user = request.user

    context = {'user': user, }

    return render(request, 'User/profile.html', context)


# def user_update(request):
#     if request.user != request.user:
#         raise Http404
#
#     user = request.user
#     user_id = UserModel.objects.get(id=user.id)
#
#     form = UserUpdateForm(instance=user_id, data=request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             new = form.save(commit=False)
#             new.phone = '+' + new.phone
#             new.save()
#
#             return redirect('userprofile:user_profile')
#
#     context = {'user': user, 'form': form}
#
#     return render(request, 'userprofile/profile.html', context)
#
#
# def change_password(request):
#     if request.user != request.user:
#         raise Http404
#
#     user_loop = UserModel.objects.all()
#     user = request.user
#
#     if request.method == 'POST':
#         user_mod = request.POST.get('id')
#         password1 = request.POST.get('password')
#         password = request.POST.get('password1')
#
#         if password1 == password:
#             user_to_change = UserModel.objects.get(id=int(user_mod))
#             user_to_change.set_password(password)
#             user_to_change.save()
#
#             return redirect('homepage')
#
#     contex = {'user_loop': user_loop, 'user': user}
#
#     return render(request, 'userprofile/password.html', contex)
#
#
# def user_change_password(request):
#     if request.user != request.user:
#         raise Http404
#
#     user = request.user
#
#     if request.method == 'POST':
#         password1 = request.POST.get('password')
#         password = request.POST.get('password1')
#
#         if password1 == password:
#             user_to_change = UserModel.objects.get(id=int(user.id))
#             user_to_change.set_password(password)
#             user_to_change.save()
#
#             return redirect('homepage')
#
#     contex = {'user': user}
#
#     return render(request, 'userprofile/change-password.html', contex)
