from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Comment

def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    return render(request, 'core/item_list.html', {'items': items, 'query': query})

def item_list_lost(request):
    items = Item.objects.filter(status='Lost').order_by('-created_at')
    query = request.GET.get('q', '')
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    return render(request, 'core/item_list.html', {'items': items, 'query': query, 'status': 'Lost'})

def item_list_found(request):
    items = Item.objects.filter(status='Found').order_by('-created_at')
    query = request.GET.get('q', '')
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    return render(request, 'core/item_list.html', {'items': items, 'query': query, 'status': 'Found'})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    comments = item.comments.filter(parent__isnull=True).order_by('created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        text = request.POST.get('text')
        if text:
            Comment.objects.create(item=item, user=request.user, text=text, parent=None)
            return redirect('core:item_detail', pk=item.pk)
            
    return render(request, 'core/item_detail.html', {'item': item, 'comments': comments})

@login_required
def item_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        status = request.POST.get('status')
        image = request.FILES.get('image')
        
        if title and status and image:
            item = Item.objects.create(
                user=request.user,
                title=title,
                description=description,
                location=location,
                status=status,
                image=image
            )
            return redirect('core:item_detail', pk=item.pk)
            
    return render(request, 'core/item_form.html')


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user != item.user:
        return redirect('core:item_detail', pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('core:item_list')
    return redirect('core:item_detail', pk=pk)


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user != item.user:
        return redirect('core:item_detail', pk=pk)
    
    if request.method == 'POST':
        item.title = request.POST.get('title', item.title)
        item.description = request.POST.get('description', item.description)
        item.location = request.POST.get('location', item.location)
        item.status = request.POST.get('status', item.status)
        
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        
        item.save()
        return redirect('core:item_detail', pk=item.pk)
    
    return render(request, 'core/item_update.html', {'item': item})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        return redirect('core:item_detail', pk=comment.item.pk)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            comment.text = text
            comment.save(update_fields=['text'])

    return redirect('core:item_detail', pk=comment.item.pk)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item_pk = comment.item.pk

    if request.user != comment.user:
        return redirect('core:item_detail', pk=item_pk)

    if request.method == 'POST':
        comment.delete()

    return redirect('core:item_detail', pk=item_pk)


@login_required
def comment_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(
                item=parent_comment.item,
                user=request.user,
                text=text,
                parent=parent_comment,
            )

    return redirect('core:item_detail', pk=parent_comment.item.pk)
