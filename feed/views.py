from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import List, Comment
from .forms import ListForm, ListItemFormSet, CommentForm


@login_required
def home_view(request):
    following_ids = set(request.user.follows_made.values_list('following_id', flat=True))
    tab = request.GET.get('tab', 'following')

    base_qs = List.objects.select_related('author', 'author__profile').prefetch_related('items', 'likes', 'comments__author')

    if tab == 'explore':
        # posts from people the user does NOT follow (excluding own posts)
        lists = base_qs.exclude(author_id__in=following_ids).exclude(author=request.user)
    else:
        # Following: own posts + posts from followed users
        in_ids = following_ids | {request.user.id}
        lists = base_qs.filter(author_id__in=in_ids)

    liked_ids = set(request.user.liked_lists.values_list('id', flat=True))
    commented_ids = set(Comment.objects.filter(author=request.user).values_list('list_id', flat=True))
    return render(request, 'feed/home.html', {
        'lists': lists,
        'liked_ids': liked_ids,
        'commented_ids': commented_ids,
        'comment_form': CommentForm(),
        'active_tab': tab,
    })


@login_required
def toggle_like_view(request, pk):
    if request.method == 'POST':
        lst = get_object_or_404(List, pk=pk)
        if request.user in lst.likes.all():
            lst.likes.remove(request.user)
        else:
            lst.likes.add(request.user)
    return redirect(request.POST.get('next', 'home'))


@login_required
def add_comment_view(request, pk):
    if request.method == 'POST':
        lst = get_object_or_404(List, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.list = lst
            comment.author = request.user
            comment.save()
    return redirect(request.POST.get('next', 'home'))


@login_required
def create_list_view(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        formset = ListItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            lst = form.save(commit=False)
            lst.author = request.user
            lst.save()
            items = formset.save(commit=False)
            for order, item in enumerate(items):
                item.list = lst
                item.order = order
                item.save()
            messages.success(request, 'Your list has been posted!')
            return redirect('home')
    else:
        form = ListForm()
        formset = ListItemFormSet()
    return render(request, 'feed/create_list.html', {'form': form, 'formset': formset})
