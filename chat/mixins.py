from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from profiles.models import Profile, Relationship


class FriendRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        followers = Relationship.objects.get_all_followers(user)
        followings = Relationship.objects.get_all_following(user)
        friends = list(set([following.receiver for following in followings] +
                           [follower.sender for follower in followers]))
        other_user = self.kwargs.get('username')
        other_user_profile = Profile.objects.get(user__username=other_user)
        if other_user_profile in friends:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(f'u are not a friend of {other_user}')
