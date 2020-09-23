from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import *
from profiles.models import Profile
from .forms import PostForm
# Create your views here.


@login_required
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    user = Profile.objects.get(user=request.user)
    print(post_id + action)
    if post_id and action:
        print('inside if')
        try:
            post = Post.objects.get(pk=int(post_id))
            print(post)
            print('got the post')
            if action == 'like':
                post.likes.create(user=user)
                print('like created')
            else:
                post.likes.get(user=user).delete()
                print('like deleted')
            return JsonResponse({'status': 'ok'})
        except:
            print('did not got the post')
            pass
    return JsonResponse({'status': 'error'})


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
def post_comment(request):
    profile = Profile.objects.get(user=request.user)
    if request.is_ajax and request.method == 'POST':
        post = Post.objects.get(id=request.POST.get('post_id'))
        comment = request.POST.get('text')
        new_comment = post.comments.create(user=profile, text=comment)
        new_comment.save()
        ser_instance = serializers.serialize(
            'json', [new_comment, profile, request.user])
        return JsonResponse({"instance": ser_instance}, status=200)
    return JsonResponse({"error": ""}, status=400)


def post_delete(request):
    pass
