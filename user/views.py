from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        name = request.POST['name']
        bio = request.POST['bio']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        
        # Validate form inputs
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        # Save avatar if provided
        avatar = None
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            fs = FileSystemStorage()
            avatar_name = fs.save(avatar.name, avatar)
            avatar_url = fs.url(avatar_name)
        else:
            avatar_url = None
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.bio = bio
        user.profile.name = name
        user.profile.mobile = mobile
        user.profile.dob = dob
        user.profile.avatar = avatar_url
        user.profile.save()
        
        return {'success': 'Account created successfully.'}
    
    return {'error': 'Only POST requests are supported.'}


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
    
    
    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login') 
    else:
        return HttpResponseNotAllowed(['POST'])
