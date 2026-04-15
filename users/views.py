from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from feed.models import List
from django.contrib.auth import update_session_auth_hash  # keep user logged in after password change
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, ProfileUpdateForm   # add ProfileUpdateForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Follow
from django.db.models import Q

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to ListShare, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    lists = List.objects.filter(author=request.user).prefetch_related('items')
    followers_count = Follow.objects.filter(followed=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()
    return render(request, 'users/profile.html', {
        'profile_user': request.user,
        'lists': lists,
        'is_own_profile': True,
        'followers_count': followers_count,
        'following_count': following_count,
    })


def user_page_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    lists = List.objects.filter(author=profile_user).prefetch_related('items')
    is_own_profile = request.user.is_authenticated and request.user == profile_user
    is_following = False
    if request.user.is_authenticated and not is_own_profile:
        is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()
    followers_count = Follow.objects.filter(followed=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'lists': lists,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
    
@login_required
@require_POST
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        messages.success(request, f"You are now following @{username}.")
    else:
        messages.error(request, "You cannot follow yourself.")
    return redirect('user_page', username=username)

@login_required
@require_POST
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    messages.success(request, f"You have unfollowed @{username}.")
    return redirect('user_page', username=username)

def search_users_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:20]  # exclude self, limit 20
    return render(request, 'users/search.html', {'query': query, 'results': results})