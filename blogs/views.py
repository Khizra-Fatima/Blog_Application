import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import BlogForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Blog, Tag, LikeDislike, Comment
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from django.core.exceptions import PermissionDenied




# Blog Creation View
@login_required
def create_new_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.publish_status = request.POST.get('status', 'draft')
            blog.save()
            form.save_m2m()

            #assign object-level permissions only when creating the blog
            assign_perm('change_blog', request.user, blog)
            assign_perm('delete_blog', request.user, blog)

            #process tags
            tag_names = {tag.name.lstrip("#") for tag in form.cleaned_data['tags']}
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)


            messages.success(request, 'Your blog has been created successfully!')
            return redirect('user_blogs', username=request.user.username)
        else:
            #print the error
            print(form.errors)
            messages.error(request, 'There was an error creating your blog. Please fix the issues and try again.')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})



# Edit a specific blog by blog_id
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the user has permission to change the blog
    if not request.user.has_perm('blogs.change_blog', blog):
        raise PermissionDenied("You do not have permission to edit this blog.")

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.publish_status = request.POST.get('status', 'draft')
            blog.save()
            form.save_m2m()

            messages.success(request, 'Your blog has been updated successfully!')
            return redirect('blog_detail', blog_id=blog.id)
        else:
            messages.error(request, 'There were errors in the form. Please correct them.')

    else:
        form = BlogForm(instance=blog)

    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, 'edit_blog.html', context)




# View all blogs created by the logged-in user
@login_required
def user_blogs(request, username):
    status_filter = request.GET.get('status', 'published')  #default to 'published'

    #get the user by username
    user = get_object_or_404(User, username=username)

    #check for both published and draft blogs
    has_blogs = Blog.objects.filter(author=user).exists()

    if status_filter == 'draft':
        blogs = Blog.objects.filter(author=request.user, publish_status='draft').order_by('-created_at')
    else:
        blogs = Blog.objects.filter(author=request.user, publish_status='published').order_by('-created_at')

    context = {
        'blogs': blogs,
        'status_filter': status_filter,
        'has_blogs': has_blogs,
        'profile_user': user 
    }

    return render(request, 'user_blogs.html', context)



# View details of a specific blog by blog_id
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    total_likes = blog.reactions.filter(reaction=1).count()
    total_dislikes = blog.reactions.filter(reaction=-1).count()
    comments = blog.comments.all()

    # Increase view count only for unique visitors
    session_key = f'viewed_blog_{blog_id}'
    if not request.session.get(session_key, False):
        blog.views += 1
        blog.save()
        request.session[session_key] = True

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'comments': comments,
    })




# Delete a specific blog by blog_id with confirmation
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the user has permission to delete the blog
    if not request.user.has_perm('blogs.delete_blog', blog):
        raise PermissionDenied("You do not have permission to delete this blog.")

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'The blog has been deleted successfully!')
        return redirect('user_blogs', username=blog.author.username)
    
    return redirect('user_blogs', username=blog.author.username)

















@login_required
@require_POST
def like_dislike_blog(request, blog_id):
    #handle reactions via AJAX.
    blog = get_object_or_404(Blog, id=blog_id)
    reaction_value = int(request.POST.get('reaction')) #1 for like, -1 for dislike
        
    #check if the user has already liked/disliked the blog
    try:
        like_dislike = LikeDislike.objects.get(user=request.user, blog=blog)

        if like_dislike.reaction == reaction_value:
            like_dislike.delete()  #if clicked again, remove the reaction
            status = 'removed'
        else:
            like_dislike.reaction = reaction_value
            like_dislike.save()
            status = 'updated'

    except LikeDislike.DoesNotExist:
        #if not found, create a new like/dislike entry
        LikeDislike.objects.create(user=request.user, blog=blog, reaction=reaction_value)
        status = 'created'


    return JsonResponse({
        'status': status,
        'total_likes': blog.reactions.filter(reaction=1).count(),
        'total_dislikes': blog.reactions.filter(reaction=-1).count(),
    })




@login_required
@require_POST
def add_comment(request, blog_id):
    #handle adding a comment via AJAX.
    blog = get_object_or_404(Blog, id=blog_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.blog = blog
        comment.save()

          
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'comment': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime("%B %d, %Y"),
        })

    return JsonResponse({'success': False, 'error': 'Invalid form submission'}, status=400)



@login_required
def user_comments(request):
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'comments.html', {'comments': comments})



@login_required
@require_POST
def edit_comment(request, comment_id):
    #handle comment editing via AJAX.
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    #parse JSON data
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()

        if not content:
            return JsonResponse({'success': False, 'error': 'Comment content cannot be empty.'})

        comment.content = content
        comment.save()

        return JsonResponse({
            'success': True,
            'updated_content': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%B %d, %Y'),
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data format.'}, status=400)



@login_required
@require_POST
def delete_comment(request, comment_id):
    #handle deleting comment via AJAX.
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()

    return JsonResponse({'success': True})