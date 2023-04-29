from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'authenticate/home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.success(request, 'Error logging in. Please try again.')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            # There are 2 password fields (double password insert.)
            # The second time the password is inserted is names 'password1'.
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been successfully registered and logged in.')
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}

    # Automated Django specific registration form created with code.
    return render(request, 'authenticate/register.html', context)
