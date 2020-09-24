from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, SearchProfileForm
from posts.forms import CommentForm

from profiles.models import Profile, Relationship
from posts.models import Post, Comment


@login_required
def profile_search_view(request):
    profiles = Profile.objects.get_all_profiles(me=request.user)
    form = SearchProfileForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchProfileForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Profile.objects.annotate(similarity=TrigramSimilarity(
                'slug', query), ). filter(similarity__gt=0.1). order_by('-similarity')
    return render(request, 'search.html', {
        'form': form,
        'query': query,
        'results': results,
        'profiles': profiles
    })


@login_required
def notifications(request):
    auth_user_profile = Profile.objects.get(user=request.user)
    follow_requests = Relationship.objects.get_all_follow_requests(
        auth_user_profile)
    return render(request, 'notifications.html', {
        'follow_requests': follow_requests
    })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, 'WELCOME {}'.format(user.username))
                    return redirect('posts:home')
                else:
                    return messages.error(request, 'This account is not active')
            else:
                return messages.error(request, "LOOK'S LIKE U DO NOT HAVE AN ACCOUNT, PLEASE SIGNUP")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {
        'form': form
    })


def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'ACCOUNT WAS SUCCESSFULLY CREATED')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/signup.html', {
        'form': form
    })


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'U WERE LOGGED OUT SUCCESSFULLY')
    return redirect('login')
