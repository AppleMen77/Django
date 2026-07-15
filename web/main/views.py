from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Post, Category, Profile, Comment, Notifications

# Create your views here.
def home(request):
    username = request.user.username
    profiles = Profile.objects.all()
    notifications = Notifications.objects.all()
    post = Post.objects.all()
    return render(request, 'main.html', {'username': username,
                                         'profiles': profiles,
                                         'posts': post,
                                         'notifications': notifications
                                         })
def profile_view(request, user_id):
    profile = Profile.objects.get(owner = user_id)
    return render(request, 'profile.html', {'profile': profile})

def login_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login (request, user)
            return redirect('/')
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('/')

def register_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username = username, password = password)
        if not user:
            user = User.objects.create_user(username, email, password)
            Profile.objects.create(owner = user,
                                    name = username)
            login(request, user)
            return redirect ('/')
    return render(request, 'register.html', {})

def cp_view(request):
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        Post.objects.create(title = title, 
                            content = content, 
                            author = request.user
                            )
        return redirect('/')
    return render(request, 'create_post.html', {})

def post_detail(request, post_id):
    post = Post.objects.get(id = post_id)
    return render(request, 'post.html', {})