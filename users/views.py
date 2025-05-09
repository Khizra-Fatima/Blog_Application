from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm, ProfileUpdateForm, EmailChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Profile
from activities.models import Bookmark
from blogs.models import LikeDislike, Comment



# User Profile_View
@login_required
def user_profile(request, username):
    if request.user.is_superuser:
        return HttpResponseForbidden("Superuser can't access this page.")

    user = get_object_or_404(User, username=username)
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('blog').order_by('-created_at')
    comments = Comment.objects.filter(user=request.user).select_related('blog').order_by('-created_at')
    likedislikes = LikeDislike.objects.filter(user=request.user).select_related('blog').order_by('-created_at')

    context = {
        'user': user,
        'bookmarks': bookmarks,  
        'likedislikes': likedislikes,
        'comments': comments,
    }
    
    return render(request, 'user_profile.html', context)



# User Edit_Profile_View
@login_required
def edit_profile(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist.")


    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(request.POST, request.user)
        email_form = EmailChangeForm(request.POST, instance=request.user)

        #handle profile dp and bio update
        if 'profile_submit' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('edit_profile', user_id=request.user.id)
            else:
                messages.error(request, 'Please correct the error below.')

        #handle Password Change
        elif 'password_submit' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('edit_profile', user_id=request.user.id)
            else:
                messages.error(request, 'Please correct the errors below.')

        #handle Email Change
        elif 'email_submit' in request.POST:
            if email_form.is_valid():
                user = email_form.save()
                messages.success(request, 'Your email has been changed successfully.')
                return redirect('edit_profile', user_id=request.user.id)
            else:
                messages.error(request, 'Please correct the errors below.')

    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)
        email_form = EmailChangeForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'email_form': email_form,
    }


    return render(request, 'edit_profile.html', context)










# User Signup_View
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create user with hashed password
            user = User.objects.create_user(username=username, email=email, password=password)

            # Authenticate the user to get the backend
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Specify backend explicitly
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# User Login_View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


# User Logout_View
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


