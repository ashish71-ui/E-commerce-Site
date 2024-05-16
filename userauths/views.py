from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .forms import LoginForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, your account is created")
            new_user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect("userauths:loginform")
    else:
        form = UserRegisterForm()

    return render(request, "userauths/sign_up.html", {'form': form})
    
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("core:index")  # Redirect to desired URL after successful login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'userauths/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect("core:base") 