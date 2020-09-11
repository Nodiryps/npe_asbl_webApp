from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Post
from .forms import PostCreationForm, PostUpdateForm
from dogs.models import Dog
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
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            form.save_m2m()
            return redirect('posts:postList')
    else:
        form = PostCreationForm(user=req.user)
    return render(req, 'posts/postCreation.html', {
            'post': None,
            'form': form,
        })


@login_required
def updatePost(req, postId):
    post = Post.objects.get(id=postId)
    if req.user == post.author:
        if req.method == 'POST':
            form = PostUpdateForm(req.POST, instance=post)
            if form.is_valid():
                form.save()
    #        post.body = req.POST['body']
     #       post.save()
            return redirect('posts:postList')
        else:
            form = PostUpdateForm(instance=post)
        return render(req, 'posts/postUpdate.html', {
            'post': post,
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
