from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Profile, Relationship
from .forms import ProfileUpdateForm

# Create your views here.


@login_required
def user_profile_detail_view(request, slug):
    curr_user_profile = Profile.objects.get(slug=slug)
    auth_user_profile = Profile.objects.get(user=request.user)

    auth_user_following = Relationship.objects.get_all_following(
        auth_user_profile.user)
    auth_user_follower = Relationship.objects.get_all_followers(
        auth_user_profile.user)

    auth_user_following_profiles = [
        following.receiver for following in auth_user_following]
    auth_user_follower_profiles = [
        follower.sender for follower in auth_user_follower]

    followings = Relationship.objects.get_all_following(
        curr_user_profile.user)
    followers = Relationship.objects.get_all_followers(
        curr_user_profile.user)

    total_followings = followings.count()
    total_followers = followers.count()

    following_profiles = [following.receiver for following in followings]
    follower_profiles = [follower.sender for follower in followers]

    requests_by_me = Relationship.objects.get_all_request_by_me(
        me=request.user)
    my_request_profiles = [i.receiver for i in requests_by_me]
    return render(request, 'profiles/profile-detail.html', {
        'curr_user_profile': curr_user_profile,
        'total_followings': total_followings,
        'total_followers': total_followers,
        'followings': followings,
        'followers': followers,
        'following_profiles': following_profiles,
        'follower_profiles': follower_profiles,
        'auth_user_profile': auth_user_profile,
        'auth_user_following_profiles': auth_user_following_profiles,
        'auth_user_follower_profiles': auth_user_follower_profiles,
        'my_request_profiles': my_request_profiles
    })


@login_required
def edit_profile_details(request, slug):
    profile = get_object_or_404(Profile, slug=slug)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST or None,
                                 request.FILES or None,
                                 instance=profile)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('profiles:profile-detail-view', kwargs={'slug': slug}))
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profiles/edit.html', {
        'form': form
    })


@login_required
def user_follow(request, slug):
    receiver = Profile.objects.get(slug=slug)
    sender = Profile.objects.get(user=request.user)
    Relationship.objects.create(
        receiver=receiver, sender=sender, status='send')
    # display message
    return HttpResponseRedirect(reverse('profiles:profile-detail-view', kwargs={'slug': slug}))


@login_required
def user_unfollow(request, slug):
    me = Profile.objects.get(user=request.user)
    other_user = Profile.objects.get(slug=slug)
    Relationship.objects.filter(
        receiver=other_user, sender=me, status='accepted').delete()
    return HttpResponseRedirect(reverse('profiles:profile-detail-view', kwargs={'slug': me.slug}))


@login_required
def confirm_follow_request(request, slug):
    me = Profile.objects.get(user=request.user)
    other_user = Profile.objects.get(slug=slug)
    Relationship.objects.filter(
        receiver=me, sender=other_user, status='send').update(status='accepted')
    return HttpResponseRedirect(reverse('notifications'))


@login_required
def delete_follow_request(request, slug):
    me = Profile.objects.get(user=request.user)
    other_user = Profile.objects.get(slug=slug)
    Relationship.objects.filter(
        receiver=me, sender=other_user, status='send').delete()
    return HttpResponseRedirect(reverse('notifications'))
