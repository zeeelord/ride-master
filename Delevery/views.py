from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from .forms import *
import requests
from .models import *


from django.db.models import Max, Sum, Avg

# from django import forms
from django.contrib.auth import get_user_model


def post_delivery(request):

    if request.user != request.user:
        raise Http404

    user = request.user

    form = PostOrderForm(request.POST, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            # new.status = '1'
            # new.user = user
            new.save()

            return redirect('Delivery:success')
    context = {'user': user, 'form': form}
    return render(request, 'Delivery/create.html', context)


def order_received(request):
    return render(request, 'Delivery/success.html')


def jobs(request):
    data = BaseModel.objects.all().order_by('-date')
    pages = Paginator(data, 6)
    # Get the page number
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)
    context = {'page': page, 'data': data}

    # print(data)

    return render(request, 'Delivery/Jobs.html', context)


def search(request):
    # requests.model
    # if requests.models == "POST":
    if request.POST.get('keyword'):
        keyword = request.POST.get('keyword')
        data = BaseModel.objects.filter(type=keyword).order_by('-date')
        pages = Paginator(data, 6)
        # Get the page number
        page_number = request.GET.get('page')
        page = pages.get_page(page_number)
    else:
        keyword = request.POST.get('key')
        data = BaseModel.objects.filter(type__contains=keyword).order_by('-date')
        pages = Paginator(data, 6)
        # Get the page number
        page_number = request.GET.get('page')
        page = pages.get_page(page_number)

    context = {'page': page, 'data': data}

    # print(data)

    return render(request, 'Delivery/Jobs.html', context)


def single(request, id):
    # requests.model
    data = BaseModel.objects.get(id=id)
    job = BaseModel.objects.filter(type='job').count()
    story = BaseModel.objects.filter(type='story').count()
    poll = BaseModel.objects.filter(type='poll').count()
    comment = BaseModel.objects.filter(type='comment').count()
    pollopt = BaseModel.objects.filter(type='pollopt').count()
    # pages = Paginator(data, 2)
    # Get the page number
    # page_number = request.GET.get('page')
    # page = pages.get_page(page_number)
    context = {'data': data, 'job': job, 'story': story, 'poll':poll, 'comment': comment, 'pollopt': pollopt}

    # print(data)

    return render(request, 'Delivery/single-post.html', context)


def update(request, id):
    # requests.model
    data = BaseModel.objects.get(id=id)
    context = {'data': data}

    if request.method == "POST":
        by = request.POST.get('by')
        title = request.POST.get('title')
        url = request.POST.get('url')
        score = request.POST.get('score')
        text = request.POST.get('tex')
        if data.type == 'job':
            BaseModel.objects.filter(pk=id).update(by=by, title=title, url=url, score=score)
        elif data.type == 'story':
            data.objects.filter(pk=id).update(by=by, title=title, url=url, score=score)
        elif data.type == 'comment':
            data.objects.filter(pk=id).update(by=by, score=score)
        elif data.type == 'poll':
            data.objects.filter(pk=id).update(by=by, title=title, text=text, score=score)
        elif data.type == 'pollopt':
            data.objects.filter(pk=id).update(by=by, text=text, score=score)

        return redirect('Delivery:single', data.id)

    # print(data)

    return render(request, 'Delivery/update.html', context)
