from django.shortcuts import render
from django.core.paginator import Paginator
from blogs.models import Blog
from activities.models import Bookmark

def home(request):
    blog_list = Blog.objects.filter(publish_status='published').order_by('-created_at')
    paginator = Paginator(blog_list, 8)  #get 8 blogs for one page

    page_number = request.GET.get('page')  #get the page number from the request
    page_obj = paginator.get_page(page_number)  #get the related page

    user_bookmark_ids = set()
    if request.user.is_authenticated:
        user_bookmark_ids = set(Bookmark.objects.filter(user=request.user).values_list('blog_id', flat=True))

    return render(request, 'home.html', {'page_obj': page_obj, 'user_bookmark_ids': user_bookmark_ids})


