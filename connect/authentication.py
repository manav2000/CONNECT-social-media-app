from django.contrib.auth.models import User


class CustomAuthBackend(object):
    """
    Authenticate with email or username
    """

    def authenticate(self, request, username=None, password=None):
        try:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
                return None
            except:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
