from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.contrib.auth.models import User

from .models import *
from profiles.models import Profile, Relationship
from .forms import PostForm, CommentForm
# Create your views here.


@login_required
def home_view(request):
    admin = User.objects.get(is_superuser=True)
    admin_prof = Profile.objects.get(user=admin)

    user = Profile.objects.get(user=request.user)

    followers = Relationship.objects.get_all_followers(user)
    followings = Relationship.objects.get_all_following(user)
    friends = list(set([following.receiver for following in followings] +
                       [follower.sender for follower in followers]))
    friends = friends + [user]

    if admin_prof not in friends:
        friends.append(admin_prof)

    posts = Post.objects.filter(user__in=friends).order_by('-created')
    form = CommentForm()

    # pagination
    # page = request.GET.get('page', 1)
    # paginator = Paginator(posts, 5)
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)

    context_data = {
        'posts': posts,
        'user': user,
        'form': form
    }
    return render(request, 'posts/posts.html', context_data)


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
            return JsonResponse({'status': 'ok', 'total_likes': post.likes.all().count()})
        except:
            print('did not got the post')
            pass
    return JsonResponse({'status': 'error'})


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


@login_required
def post_delete(request):
    post_id = request.POST.get('id')
    try:
        post = Post.objects.get(pk=int(post_id))
        post.delete()
        return JsonResponse({'status': 'ok'})
    except:
        pass
    return JsonResponse({'error': 'error'})


# @login_required
# def post_save(request, id):
#     post = Post.objects.get(id=id)
#     user = Profile.objects.get(user=request.user)
#     post.saved.create(user=user)
#     return HttpResponseRedirect(reverse('home'))


# @login_required
# def post_unsave(request, id):
#     post = Post.objects.get(id=id)
#     user = Profile.objects.get(user=request.user)
#     post.saved.get(user=user).delete()
#     return HttpResponseRedirect(reverse('home'))
