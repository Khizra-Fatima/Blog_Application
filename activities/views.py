from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Bookmark
from django.contrib import messages








@login_required
def bookmark_blog(request, blog_id):
    if request.user.is_superuser:
        return JsonResponse({"error": "Superusers are not allowed to bookmark."}, status=403)

    bookmark, created = Bookmark.objects.get_or_create(user=request.user, blog_id=blog_id)

    if created:
        return JsonResponse({'status': 'bookmarked'})
    else:
        bookmark.delete()
        return JsonResponse({'status': 'removed'})

    


@login_required
def bookmarked_blog(request):
    bookmarked = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmarks.html', {'bookmarked': bookmarked})




@login_required
def delete_bookmark_blog(request, bookmark_id):
    if request.method == 'POST':
        bookmark_blog = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
        bookmark_blog.delete()
        messages.success(request, 'Item deleted successfully!')
    
    return redirect('bookmarked_blog')




@login_required
def clear_bookmark(request):
    if request.method == 'POST':
        Bookmark.objects.filter(user=request.user).delete()
        messages.success(request, 'All items have been removed from your Bookmark List!')

    return redirect('bookmarked_blog')





