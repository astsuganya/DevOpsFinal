from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from core.models import Item, Comment

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:item_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user_items = Item.objects.filter(user=request.user).order_by('-created_at')
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    stats = {
        'items_count': user_items.count(),
        'comments_count': user_comments.count(),
        'lost_count': user_items.filter(status='Lost').count(),
        'found_count': user_items.filter(status='Found').count(),
    }
    return render(
        request,
        'accounts/profile.html',
        {
            'user_items': user_items,
            'user_comments': user_comments,
            'stats': stats,
        },
    )


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change_form.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('core:item_list')

    return render(request, 'accounts/account_delete_confirm.html')
