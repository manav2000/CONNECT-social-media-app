from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import Thread, Message
from profiles.models import Profile, Relationship
from django.contrib.auth.models import User

from .mixins import FriendRequiredMixin

# Create your views here.


@login_required
def friends_list_to_chat(request):
    user = Profile.objects.get(user=request.user)
    followers = Relationship.objects.get_all_followers(user)
    followings = Relationship.objects.get_all_following(user)
    friends = list(set([following.receiver for following in followings] +
                       [follower.sender for follower in followers]))
    return render(request, 'chat/friends.html', {
        'friends': friends,
    })


class ThreadView(LoginRequiredMixin, FriendRequiredMixin, View):
    template_name = 'chat/chat.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(
            self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['me'] = self.request.user
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = self.get_object().message_set.all()
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    # def post(self, request, **kwargs):
    #     self.object = self.get_object()
    #     thread = self.get_object()
    #     data = request.POST
    #     user = request.user
    #     text = data.get("message")
    #     Message.objects.create(sender=user, thread=thread, text=text)
    #     context = self.get_context_data(**kwargs)
    #     return render(request, self.template_name, context=context)
