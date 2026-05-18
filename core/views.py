from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Comment

def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'core/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    comments = item.comments.all().order_by('created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        text = request.POST.get('text')
        if text:
            Comment.objects.create(item=item, user=request.user, text=text)
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
