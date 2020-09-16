from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Profile, Relationship

# Create your views here.


@login_required
def user_profile_detail_view(request, slug):
    user_profile = Profile.objects.get(slug=slug)
    auth_user_profile = Profile.objects.get(user=request.user)
    auth_user_following = Relationship.objects.get_all_following(
        auth_user_profile.user)
    auth_user_following_profiles = [
        following.receiver for following in auth_user_following]
    followings = Relationship.objects.get_all_following(
        user_profile.user)
    followers = Relationship.objects.get_all_followers(
        user_profile.user)
    total_followings = followings.count()
    total_followers = followers.count()
    following_profiles = [following.sender for following in followings]
    follower_profiles = [follower.receiver for follower in followers]
    return render(request, 'profiles/profile-detail.html', {
        'user_profile': user_profile,
        'total_followings': total_followings,
        'total_followers': total_followers,
        'followings': followings,
        'followers': followers,
        'following_profiles': following_profiles,
        'follower_profiles': follower_profiles,
        'auth_user_profile': auth_user_profile,
        'auth_user_following_profiles': auth_user_following_profiles
    })
