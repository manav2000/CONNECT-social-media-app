from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, SearchProfileForm, ResetPassword
from posts.forms import CommentForm

from profiles.models import Profile, Relationship
from posts.models import Post, Comment

from .decorators import unauthenticated_user


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
    follow_requests = Relationship.objects.filter(
        receiver__user=request.user, status='send')
    return render(request, 'notifications.html', {
        'follow_requests': follow_requests
    })


@unauthenticated_user
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
                    messages.error(request, 'THIS ACCOUNT IS NOT ACTIVE')
                    return redirect('login')
            else:
                messages.error(
                    request, "INVALID LOGIN CREDENTIAL'S")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {
        'form': form
    })


@unauthenticated_user
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


@unauthenticated_user
def reset_password(request):
    if request.method == 'POST':
        form = ResetPassword(data=request.POST)

        if(form.is_valid()):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, "PASSWORD RESET WAS SUCCESSFULL")
            return HttpResponseRedirect(reverse('login'))

    else:
        form = ResetPassword()

    return render(request, 'auth/reset_pwd.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'U WERE LOGGED OUT SUCCESSFULLY')
    return redirect('login')
