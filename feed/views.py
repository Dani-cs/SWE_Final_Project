from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import List
from .forms import ListForm, ListItemFormSet
from django.db.models import Q


@login_required
def home_view(request):
    # Get users that current user follows
    following_ids = request.user.following.values_list('followed_id', flat=True)
    # Show own lists + lists from followed users
    lists = List.objects.filter(
        Q(author=request.user) | Q(author_id__in=following_ids)
    ).select_related('author').prefetch_related('items').order_by('-created_at')
    return render(request, 'feed/home.html', {'lists': lists})

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
