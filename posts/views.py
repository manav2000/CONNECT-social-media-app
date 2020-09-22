from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from profiles.models import Profile
from .forms import PostForm
# Create your views here.


@login_required
def post_like(request, id):
    post = Post.objects.get(id=id)
    user = Profile.objects.get(user=request.user)
    post.likes.create(user=user)
    return HttpResponseRedirect(reverse('home'))


@login_required
def post_unlike(request, id):
    post = Post.objects.get(id=id)
    user = Profile.objects.get(user=request.user)
    post.likes.get(user=user).delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def post_save(request, id):
    post = Post.objects.get(id=id)
    user = Profile.objects.get(user=request.user)
    post.saved.create(user=user)
    return HttpResponseRedirect(reverse('home'))


@login_required
def post_unsave(request, id):
    post = Post.objects.get(id=id)
    user = Profile.objects.get(user=request.user)
    post.saved.get(user=user).delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def post_comment(request, id):
    profile = Profile.objects.get(user=request.user)
    post = Post.objects.get(id=id)
    comment = request.POST.get('text')
    if comment:
        post.comments.create(user=profile, text=comment)
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


def post_delete(request):
    pass
