from profiles.models import Profile, Relationship


def user_profile_context(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        return {'user_profile': user_profile}
    except:
        return {}
