from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def allusers(user):
    if user.role == 'Super Admin' or user.role ==  'Teacher' or user.role == 'Clerk' or user.role == 'Peon':
        return True

def mangagement(user):
    if user.role == 'Super Admin' or user.role == 'Clerk':
        return True


def superadmin(user):
    if user.role == 'Super Admin':
        return True

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'landings/login/loginpage.html', {'msg': 'Invalid credentials, please try again.'})
            
    return render(request, 'landings/login/loginpage.html')



