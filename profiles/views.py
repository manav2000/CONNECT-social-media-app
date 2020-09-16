from django.shortcuts import render
from .models import Profile, Relationship

# Create your views here.


def user_profile_detail_view(request, slug):
    user_profile = Profile.objects.get(user=request.user)
    followings = Relationship.objects.get_all_following(request.user).count()
    followers = Relationship.objects.get_all_followers(request.user).count()
    return render(request, 'profiles/profile-detail.html', {
        'user_profile': user_profile,
        'followings': followings,
        'followers': followers
    })
