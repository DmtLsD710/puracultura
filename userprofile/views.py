from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page or home page after successful registration
            return redirect('userprofile:login')
    else:
        form = SignupForm()
    return render(request, 'userprofile/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')  # Make sure 'home' is a valid URL name
    else:
        form = LoginForm()
    return render(request, 'userprofile/login.html', {'form': form})
