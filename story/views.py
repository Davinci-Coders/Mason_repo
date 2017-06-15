# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone

from story.models import Post
from story.forms import PostForm


def home(request):
    return render(request, 'base.html')


def story(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog_homepage.html', context)


def specific(request, blog_id):
    context = {
        'post': Post.objects.get(id=blog_id)
    }
    return render(request, 'specific_blogpage.html', context)


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            context = {
                'posts': Post.objects.all()
            }
            return render(request, 'blog_homepage.html', context)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # print 'form is post'
        form = AuthenticationForm(request.POST)
        # if form.is_valid():
        print 'form is valid'
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'base.html')
        else:
            print 'User could not login'
        # else:
        #     print 'Form not valid'
        #     import ipdb
        #     ipdb.set_trace()
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
