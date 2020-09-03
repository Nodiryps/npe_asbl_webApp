from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db import models
from django.views.generic import View
from .models import Post
from .forms import PostCreationForm
from dogs.models import Dog
from accounts.models import User
import json


@login_required
def postList(req):
    if isUserAllowed(req.user):
        posts = Post.objects.all().order_by('timestamp')

        return render(req, 'posts/postList.html', {
            'isUserAllowed': isUserAllowed(req.user),
            'isPostContent': True,
            'posts': posts,
            'form': PostCreationForm(user=req.user),
        })
    else:
        return redirect('home')


def isUserAllowed(currUser):
    if currUser.is_admin:
        return True
    else:
        return True if currUser.isOwner or currUser.isHost or currUser.isSponsor else False


@login_required
def createPost(req):
    if req.method == 'POST':
        form = PostCreationForm(req.POST, req.FILES, user=req.user)
        if form.is_valid():
            form.save()
            return redirect('posts:postList')
    else:
        form = PostCreationForm(user=req.user)
    return render(req, 'posts/postCreation.html', {
            'post': None,
            'form': form,
        })


def ajaxRender(req, template, contxt):
    html = render_to_string(
        template_name=template,
        context=contxt
    )
    data_dict = {'html_from_view': html}

    return JsonResponse(data=data_dict, safe=False)


@login_required
def createPostAjax(req, dog, body, pict):
    post = Post(dog=dog, postPicture=req.FILES, author=req.user, body=body)
    post.save()
    ajaxRender(req, 'posts/postList.html', {
        'isUserAllowed': isUserAllowed(req.user),
        'isPostContent': True,
        'posts': Post.objects.all().order_by('timestamp'),
        'form': PostCreationForm(user=req.user),
    })


# class createPost(View):
#     def get(self, req):
#         dogName = req.GET.get('dogNamesList', None)
#         body = req.GET.get('body', None)
#         picture = req.GET.get('postPicture', None)
#         dog = Dog.objects.values_list('name', flat=True).get(name=dogName)

#         obj = Post.objects.create(dog=dog, body=body, postPicture=picture)
#         post = {'id': obj.id}
#         print('\nPOST:::', post)

#         data = {'post': post}

#         return JsonResponse(data)


# def savePost(req, form, template):
#     data = {}
#     if req.method == 'POST':
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             posts = Post.objects.all().order_by('timestamp')
#             data['postList'] = render_to_string(template', {
#                 'isUserAllowed': isUserAllowed(req.user),
#                 'isPostContent': True,
#                 'posts': posts
#             })
#         else:
#             data['validForm'] = False
#     context = {'form': form}
#     data['form'] = render_to_string(template, context, request=req)
#     return JsonResponse(data)


# def createPost(req):
#     form = PostCreationForm()
#     if req.method == 'POST':
#         form = PostCreationForm(req.POST, req.FILES)
#     return savePost(req, form, 'posts/postList.html')