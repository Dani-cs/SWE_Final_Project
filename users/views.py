from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, ProfileUpdateForm
from .models import Follow, UserProfile, AVATAR_COLORS
from feed.models import List, Comment
from feed.forms import CommentForm


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


def _profile_context(request, profile_user, is_own_profile):
    lists = List.objects.filter(author=profile_user).select_related('author', 'author__profile').prefetch_related('items', 'likes', 'comments__author')
    liked_lists = profile_user.liked_lists.select_related('author', 'author__profile').prefetch_related('items', 'likes', 'comments__author').order_by('-created_at')
    commented_lists = List.objects.filter(comments__author=profile_user).distinct().select_related('author', 'author__profile').prefetch_related('items', 'likes', 'comments__author').order_by('-created_at')

    followers_count = profile_user.follows_received.count()
    following_count = profile_user.follows_made.count()

    if request.user.is_authenticated:
        liked_ids = set(request.user.liked_lists.values_list('id', flat=True))
        commented_ids = set(Comment.objects.filter(author=request.user).values_list('list_id', flat=True))
        viewer_following_ids = set(request.user.follows_made.values_list('following_id', flat=True))
        is_following = profile_user.id in viewer_following_ids
        follows_you = Follow.objects.filter(follower=profile_user, following=request.user).exists()
    else:
        liked_ids = set()
        commented_ids = set()
        viewer_following_ids = set()
        is_following = False
        follows_you = False

    return {
        'profile_user': profile_user,
        'lists': lists,
        'liked_lists': liked_lists,
        'commented_lists': commented_lists,
        'is_own_profile': is_own_profile,
        'liked_ids': liked_ids,
        'commented_ids': commented_ids,
        'comment_form': CommentForm(),
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'follows_you': follows_you,
    }


@login_required
def profile_view(request):
    ctx = _profile_context(request, request.user, is_own_profile=True)
    return render(request, 'users/profile.html', ctx)


def user_page_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own = request.user.is_authenticated and request.user == profile_user
    ctx = _profile_context(request, profile_user, is_own_profile=is_own)
    return render(request, 'users/profile.html', ctx)


def followers_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    follower_ids = profile_user.follows_received.values_list('follower_id', flat=True)
    followers = User.objects.filter(pk__in=follower_ids).select_related('profile')
    viewer_following_ids = set(request.user.follows_made.values_list('following_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'users/user_list.html', {
        'profile_user': profile_user,
        'users': followers,
        'list_type': 'followers',
        'viewer_following_ids': viewer_following_ids,
    })


def following_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    following_ids = profile_user.follows_made.values_list('following_id', flat=True)
    following = User.objects.filter(pk__in=following_ids).select_related('profile')
    viewer_following_ids = set(request.user.follows_made.values_list('following_id', flat=True)) if request.user.is_authenticated else set()
    return render(request, 'users/user_list.html', {
        'profile_user': profile_user,
        'users': following,
        'list_type': 'following',
        'viewer_following_ids': viewer_following_ids,
    })


@login_required
def settings_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        color = request.POST.get('avatar_color', '')
        if color in AVATAR_COLORS:
            profile.avatar_color = color
            profile.save()
            messages.success(request, 'Avatar color updated!')
        return redirect('settings')
    return render(request, 'users/settings.html', {
        'profile': profile,
        'avatar_colors': AVATAR_COLORS,
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


def search_users_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:20] if request.user.is_authenticated else User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )[:20]
    return render(request, 'users/search.html', {'query': query, 'results': results})


@login_required
def toggle_follow_view(request, username):
    if request.method == 'POST':
        target = get_object_or_404(User, username=username)
        if target != request.user:
            follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
            if not created:
                follow.delete()
    return redirect(request.POST.get('next', 'home'))
